middleprev = "Middle click to find previous"
scroll = "Right click to scroll one step. Middle click to auto-scroll. Wheel to scroll"

tips = {
    "main_menu": "Open the main menu",
    "model_menu": "Open the model menu",
    "more_menu": "Show more options",
    "load_button": "Load or unload the model",
    "scroller_button": "Scroll this row. Middle click for instant",
    "stop_button": "Stop generating the current response",
    "new_button": "Make a new tab. Middle click to insert at the start",
    "clear_button": "Clear the conversation",
    "close_button": "Close tabs. Middle click to close all tabs",
    "top_button": f"Scroll to the top. {scroll}",
    "bottom_button": f"Scroll to the bottom. {scroll}",
    "clear_input_button": "Clear the input",
    "prev_button": "Previous item in the input history",
    "next_button": "Next item in the input history",
    "write_button": "Show a textbox for longer inputs. Middle click to maximize",
    "submit_button": "Send the prompt to the AI. Middle click to avoid using history",
    "browse_file_button": "Browse for a file to use",
    "open_file_button": "Open the current file",
    "recent_files_button": "Show a list of files used recently",
    "user": "Personalize yourself",
    "ai": "Personalize the AI",
    "input": (
        " This is a message that the AI will respond to."
        " Use up/down arrows to cycle input history."
        " You can also use commands here. See /commands"
    ),
    # System
    "system_cpu": "Current CPU usage",
    "system_ram": "Current RAM usage",
    "system_temp": "Current CPU temperature",
    "system_gpu": "Current GPU usage",
    "system_gpu_ram": "Current GPU RAM usage",
    "system_gpu_temp": "Current GPU temperature",
    # Model state
    "model_unloaded": "No model is loaded. Pick a local or GPT model to start chatting",
    "model_remote": (
        "You are using a remote service."
        " Its usage might cost money. Internet connection is required"
    ),
    "model_local": "You are using a local model. No network requests are made",
    # Config
    "model": (
        "Path to a model file. This should be a file that works with"
        " llama.cpp, like gguf files for instance. It can also be a specific ChatGPT model."
        " Check the main menu on the right to load the available models"
    ),
    "avatar_user": "The avatar of the user (You)",
    "name_user": "The name of the user (You)",
    "avatar_ai": "The avatar of the AI",
    "name_ai": "The name of the AI",
    "history": (
        "The number of previous messages to include in the prompt."
        " The computation will take longer with more history."
        " 0 means history is not used at all"
    ),
    "context": (
        "The context size is the maximum number of tokens that the model can account for"
        " when processing a response. This includes the prompt, and the response itself"
    ),
    "max_tokens": (
        "Maximum number of tokens to generate."
        " Higher values will result in longer output, but will"
        " also take longer to compute"
    ),
    "threads": "The number of CPU threads to use",
    "gpu_layers": (
        "Number of layers to offload to GPU. If -1, all layers are offloaded."
        " More layers should speed up response time significantly."
        " Use enough layers to almost fill the GPU memory but no more"
    ),
    "format": (
        "That will format the prompt according to how model expects it."
        " Auto is supposed to work with newer models that include the format in the metadata."
        " Check llama-cpp-python to find all the available formats"
    ),
    "temperature": (
        "The temperature parameter is used to control"
        " the randomness of the output. A higher temperature (~1) results in more randomness"
        " and diversity in the generated text, as the model is more likely to"
        " explore a wider range of possible tokens. Conversely, a lower temperature"
        " (<1) produces more focused and deterministic output, emphasizing the"
        " most probable tokens"
    ),
    "seed": (
        "The seed to use for sampling."
        " The same seed should generate the same or similar results."
        " -1 means no seed is used"
    ),
    "top_p": (
        "Top-p, also known as nucleus sampling, controls"
        " the cumulative probability of the generated tokens."
        " The model generates tokens until the cumulative probability"
        " exceeds the chosen threshold (p). This approach allows for"
        " more dynamic control over the length of the generated text"
        " and encourages diversity in the output by including less"
        " probable tokens when necessary"
    ),
    "top_k": (
        "(Not applied to GPT) The Top-k parameter limits the model's"
        " predictions to the top k most probable tokens at each step"
        " of generation. By setting a value for k, you are instructing"
        " the model to consider only the k most likely tokens."
        " This can help in fine-tuning the generated output and"
        " ensuring it adheres to specific patterns or constraints"
    ),
    "stop": (
        "A list of strings to stop generation when encountered."
        " Separate each item with ;;"
    ),
    "mlock": "Keep the model in memory",
    "logits": "Enable logits for all tokens. This might make it slower but can fix some problems",
    "before": "Add this to the beginning of the prompt",
    "after": "Add this to the end of the prompt",
    "mode": (
        "The mode of the model. Either text or image."
        " On image mode, the model is able to analyse image paths you give it"
    ),
    "file": "The URL or path to a file",
    # Find
    "find_next_i": f"Find next match (case insensitive). {middleprev}",
    "find_next": f"Find next match (case sensitive). {middleprev}",
    "find_bound_i": f"Find next word-bound match (case insensitive). {middleprev}",
    "find_bound": f"Find next word-bound match (case sensitive). {middleprev}",
    "find_hide": "Hide the find bar (Esc)",
    "auto_scroll_slower": "Decrease the auto-scroll speed",
    "auto_scroll": "Toggle auto-scroll",
    "auto_scroll_faster": "Increase the auto-scroll speed",
}
