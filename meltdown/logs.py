from __future__ import annotations

# Standard
import json
from pathlib import Path

# Modules
from .app import app
from .config import config
from .dialogs import Dialog, Commands
from .display import display
from .args import args
from .session import session
from .session import Conversation
from .paths import paths
from .utils import utils
from .files import files
from .formats import formats
from .memory import memory


class Logs:
    def __init__(self) -> None:
        self.separator = "---"

    def menu(self) -> None:
        cmds = Commands()
        cmds.add("Open", lambda a: self.open_directory())
        cmds.add("Last", lambda a: self.open_last_log())
        cmds.add("Save", lambda a: self.save_menu())

        Dialog.show_dialog("Logs Menu", commands=cmds)

    def save_menu(self, full: bool = True, tab_id: str | None = None) -> None:
        cmds = Commands()

        if full:
            cmds.add("Save All", lambda a: self.save_all())

        cmds.add("Markdown", lambda a: self.to_markdown(tab_id=tab_id))
        cmds.add("JSON", lambda a: self.to_json(tab_id=tab_id))
        cmds.add("Text", lambda a: self.to_text(tab_id=tab_id))

        Dialog.show_dialog("Save conversation to a file?", cmds)

    def save_all(self) -> None:
        cmds = Commands()
        cmds.add("Markdown", lambda a: self.to_markdown(True))
        cmds.add("JSON", lambda a: self.to_json(True))
        cmds.add("Text", lambda a: self.to_text(True))

        Dialog.show_dialog("Save all conversations?", cmds)

    def save_file(
        self, text: str, name: str, ext: str, save_all: bool, overwrite: bool, mode: str
    ) -> str:
        text = text.strip()
        paths.logs.mkdir(parents=True, exist_ok=True)
        file_name = name + f".{ext}"
        file_path = Path(paths.logs, file_name)
        num = 2

        if (not overwrite) and args.increment_logs:
            while file_path.exists():
                file_name = f"{name}_{num}.{ext}"
                file_path = Path(paths.logs, file_name)
                num += 1

                if num > 9999:
                    break

        files.write(file_path, text)

        if not save_all:
            if not args.quiet and args.log_feedback:
                utils.saved_path(file_path)

            cmd = ""

            if args.open_on_log:
                app.open_generic(str(file_path))
            else:
                if (mode == "text") and args.on_log_text:
                    cmd = args.on_log_text
                elif (mode == "json") and args.on_log_json:
                    cmd = args.on_log_json
                elif (mode == "markdown") and args.on_log_markdown:
                    cmd = args.on_log_markdown
                elif args.on_log:
                    cmd = args.on_log

                if cmd:
                    app.run_program(cmd, str(file_path))

        return str(file_path)

    def save(
        self,
        mode: str,
        save_all: bool,
        name: str | None = None,
        tab_id: str | None = None,
    ) -> None:
        num = 0
        last_log = ""
        ext = formats.get_ext(mode)
        overwrite = bool(name)

        def save(content: str, name_: str) -> None:
            nonlocal num, last_log

            if not content:
                return

            num += 1

            if args.clean_names:
                name_ = utils.clean_name(name_)

            name_ = name_[: config.max_file_name_length].strip(" _")

            last_log = self.save_file(
                content, name_, ext, save_all, overwrite=overwrite, mode=mode
            )

        if save_all:
            conversations = [
                session.get_conversation(key) for key in session.conversations
            ]
        else:
            tabconvo = display.get_tab_convo(tab_id)

            if not tabconvo:
                return

            conversations = [tabconvo.convo]

        if (len(conversations) > 1) and args.concat_logs:
            contents = []

            for conversation in conversations:
                if not conversation:
                    continue

                if not conversation.items:
                    continue

                contents.append(self.get_content(mode, conversation))

            if mode == "text":
                content = f"\n\n{self.separator}\n\n".join(contents)
            elif mode == "json":
                cont = "[\n" + ",\n".join(contents) + "\n]"
                content = json.dumps(json.loads(cont), indent=4)
            elif mode == "markdown":
                content = f"\n\n{self.separator}\n\n".join(contents)
            else:
                content = ""

            name_ = f"{len(contents)}_{utils.random_word()}"
            save(content, name_)
        else:
            for conversation in conversations:
                if not conversation:
                    continue

                if not conversation.items:
                    continue

                content = self.get_content(mode, conversation)
                name_ = name or conversation.name
                save(content, name_)

        if save_all:
            if args.quiet or (not args.log_feedback):
                return

            f_type = formats.get_name(mode)
            word = utils.singular_or_plural(num, "log", "logs")
            msg = f"{num} {f_type} {word} saved."
            display.print(utils.emoji_text(msg, "storage"))

        if last_log:
            memory.set_value("last_log", last_log)

    def to_json(
        self,
        save_all: bool = False,
        name: str | None = None,
        tab_id: str | None = None,
    ) -> None:
        self.save("json", save_all, name, tab_id=tab_id)

    def to_markdown(
        self,
        save_all: bool = False,
        name: str | None = None,
        tab_id: str | None = None,
    ) -> None:
        self.save("markdown", save_all, name, tab_id=tab_id)

    def get_json(self, conversation: Conversation) -> str:
        if not conversation:
            return ""

        if not conversation.items:
            return ""

        return formats.get_json(conversation, name_mode="log")

    def get_models(self, conversation: Conversation) -> list[str]:
        """Return unique model names used in the conversation, preserving order."""
        models: list[str] = []
        seen: set[str] = set()

        # Safeguard if conversation or items are missing
        if not conversation or not getattr(conversation, "items", None):
            return models

        for it in conversation.items:
            m = getattr(it, "model", None)
            if m and (m not in seen):
                models.append(m)
                seen.add(m)

        return models

    def build_model_refs(
        self, conversation: Conversation
    ) -> tuple[list[str], dict[str, int]]:
        """Return header label list and a mapping model->index (1-based)."""
        models = self.get_models(conversation)
        ref_map: dict[str, int] = {m: i + 1 for i, m in enumerate(models)}
        # Use full model strings for logs (less ambiguous)
        header_labels = [f"{m} ({ref_map[m]})" for m in models]
        return header_labels, ref_map

    def normalize_label(self, label: str) -> str:
        """Strip spaces and a possible trailing colon from a label."""
        s = label.strip()
        if s.endswith(":"):
            s = s[:-1].rstrip()
        return s

    def build_body_with_refs(
        self, conversation: Conversation, ref_map: dict[str, int]
    ) -> str:
        """Construct body text for logs including per-AI model references."""
        # Use display prompts for consistent labels (no colons/spaces), then add our own
        user_label = self.normalize_label(
            display.get_prompt("user", put_colons=False, colon_space=False)
        )

        ai_label_base = self.normalize_label(
            display.get_prompt("ai", put_colons=False, colon_space=False)
        )

        blocks: list[str] = []

        for it in conversation.items:
            item_lines: list[str] = []

            # User message
            if getattr(it, "user", None):
                utext = it.user.rstrip() if isinstance(it.user, str) else it.user
                item_lines.append(f"{user_label}: {utext}")

                file = getattr(it, "file", None)
                if file:
                    # single blank line before file path only if there is previous content
                    if item_lines:
                        item_lines.append("")
                    item_lines.append(f"File: {file}")

            # AI message with model reference (use AI alias + (n))
            if getattr(it, "ai", None):
                model_name = getattr(it, "model", None)
                ref_num = ref_map.get(model_name or "", None)

                if ref_num is not None:
                    ai_label = f"{ai_label_base} ({ref_num})"
                else:
                    ai_label = ai_label_base

                atext = it.ai.rstrip() if isinstance(it.ai, str) else it.ai

                # Add a blank line if there was user content before this
                if item_lines:
                    item_lines.append("")

                item_lines.append(f"{ai_label}: {atext}")

            # Commit this item's block
            # Remove any leading/trailing empties inside the block
            while item_lines and (item_lines[0] == ""):
                item_lines.pop(0)

            while item_lines and (item_lines[-1] == ""):
                item_lines.pop()

            if item_lines:
                # Collapse any accidental multiple blank lines inside the block
                collapsed: list[str] = []
                prev_blank = False

                for ln in item_lines:
                    if ln == "":
                        if not prev_blank:
                            collapsed.append(ln)
                        prev_blank = True
                    else:
                        collapsed.append(ln)
                        prev_blank = False

                blocks.append("\n".join(collapsed))

        # Join items with the separator
        return f"\n\n{self.separator}\n\n".join(blocks)

    def to_text(
        self,
        save_all: bool = False,
        name: str | None = None,
        tab_id: str | None = None,
    ) -> None:
        self.save("text", save_all, name, tab_id=tab_id)

    def get_text(self, conversation: Conversation) -> str:
        if not conversation:
            return ""

        if not conversation.items:
            return ""

        # Determine model/reference behavior up-front
        models = self.get_models(conversation)
        multi_models = len(models) > 1
        log_refs = getattr(args, "log_references", True)

        header_labels: list[str] | None = None

        if multi_models and log_refs:
            # Build both header labels and body once using the same mapping
            header_labels, ref_map = self.build_model_refs(conversation)
            text = self.build_body_with_refs(conversation, ref_map=ref_map)
        else:
            # Build base content using existing formatter
            text = formats.get_text(conversation, name_mode="log")
            if not text:
                return ""

        full_text = ""
        full_text += f"Name: {conversation.name}\n"

        date_created = utils.to_date(conversation.created)
        full_text += f"Created: {date_created}\n"

        if models:
            if multi_models and log_refs:
                # header_labels computed above in the branch
                if header_labels is None:
                    header_labels, _ = self.build_model_refs(conversation)
                full_text += f"Models: {', '.join(header_labels)}\n"
            else:
                full_text += f"Models: {', '.join(models)}\n"

        date_saved = utils.to_date(utils.now())
        full_text += f"Saved: {date_saved}"

        full_text += f"\n\n{self.separator}\n\n"
        full_text += text

        return full_text

    def get_markdown(self, conversation: Conversation) -> str:
        if not conversation:
            return ""

        if not conversation.items:
            return ""

        # Determine model/reference behavior up-front
        models = self.get_models(conversation)
        multi_models = len(models) > 1
        log_refs = getattr(args, "log_references", True)
        header_labels: list[str] | None = None

        if multi_models and log_refs:
            # Build both header labels and body once using the same mapping
            header_labels, ref_map = self.build_model_refs(conversation)
            text = self.build_body_with_refs(conversation, ref_map=ref_map)
        else:
            # Build base content using existing formatter
            text = formats.get_markdown(conversation, name_mode="log")

            if not text:
                return ""

        full_text = ""
        full_text += f"# {conversation.name}\n\n"

        date_created = utils.to_date(conversation.created)
        full_text += f"**Created:** {date_created}\n"

        if models:
            if multi_models and log_refs:
                if header_labels is None:
                    header_labels, _ = self.build_model_refs(conversation)
                full_text += f"**Models:** {', '.join(header_labels)}\n"
            else:
                full_text += f"**Models:** {', '.join(models)}\n"

        date_saved = utils.to_date(utils.now())
        full_text += f"**Saved:** {date_saved}"

        full_text += f"\n\n{self.separator}\n\n"
        full_text += text

        return full_text

    def open_last_log(self) -> None:
        if not memory.last_log:
            return

        app.open_generic(memory.last_log)

    def get_content(self, mode: str, conversation: Conversation) -> str:
        if mode == "text":
            text = self.get_text(conversation)
        elif mode == "json":
            text = self.get_json(conversation)
        elif mode == "markdown":
            text = self.get_markdown(conversation)
        else:
            text = ""

        return text.strip()

    def open_directory(self) -> None:
        paths.logs.mkdir(parents=True, exist_ok=True)
        app.open_generic(str(paths.logs))


logs = Logs()
