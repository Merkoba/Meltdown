# Modules
from .args import args
from .session import Conversation


def to_text(conversation: Conversation) -> str:
    avatars = args.avatars_in_logs
    separate = args.separate_logs
    files = args.files_in_logs
    names = args.names_in_logs

    return conversation.to_text(
        avatars=avatars, names=names, separate=separate, files=files
    )


def to_markdown(conversation: Conversation) -> str:
    avatars = args.avatars_in_logs
    separate = args.separate_logs
    files = args.files_in_logs
    names = args.names_in_logs

    return conversation.to_markdown(
        avatars=avatars, names=names, separate=separate, files=files
    )


def to_json(conversation: Conversation) -> str:
    ensure_ascii = args.ascii_logs
    return conversation.to_json(ensure_ascii=ensure_ascii)
