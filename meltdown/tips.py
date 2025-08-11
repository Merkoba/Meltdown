middleprev = "Middle click to find previous"
scroll = "Right click to scroll one step. Wheel to scroll. Middle click to autoscroll"
tab_btns = "Shift click to scroll. Ctrl click to move"

tips = {
    "main_menu": "Open the main menu",
    "model_menu": "Open the model menu",
    "tab_menu": "Show the tabs menu\nMiddle click to show the tab list",
    "more_menu": "Show more options\nMiddle click to upload",
    "load_button": "Load or unload the model",
    "scroller_button": "Scroll this row. Middle click for instant",
    "stop_button": "Stop generating the current response",
    "new_button": "Make a new tab. Middle click to insert at the start",
    "clear_button": "Clear the conversation",
    "close_button": "Close tabs. Middle click to close all. Shift click to close empty. Ctrl click to close old",
    "top_button": f"Scroll to the top. {scroll}",
    "bottom_button": f"Scroll to the bottom. {scroll}. Right click to go to the top",
    "clear_input_button": "Clear the input",
    "prev_button": "Previous item in the input history",
    "next_button": "Next item in the input history",
    "write_button": "Write an elaborate input. Middle click to maximize",
    "submit_button": "Submit the input. Middle click to avoid using history",
    "browse_file_button": "Browse for a file to use",
    "open_file_button": "Open the current file",
    "recent_files_button": "Show a list of files used recently",
    "user": "Personalize yourself",
    "ai": "Personalize the AI",
    "input": (
        " Write a message that the AI will respond to."
        " Use up/down arrows to cycle input history."
        " You can also use commands here. See /commands"
    ),
    "recent_input_button": "Show a list of recent inputs",
    "toggle_file_button": "Toggle the file frame",
    # System
    "system_cpu": "Current CPU usage",
    "system_ram": "Current RAM usage",
    "system_temp": "Current CPU temperature",
    "system_gpu": "Current GPU usage",
    "system_gpu_ram": "Current GPU RAM usage",
    "system_gpu_temp": "Current GPU temperature",
    # Model state
    "model_unloaded": "No model is loaded.\nPick a local or remote model to start chatting",
    "model_remote": (
        "You are using a remote service."
        "\nIts usage might cost money."
        "\nInternet connection is required"
    ),
    "model_local": "You are using a local model.\nInternet is not required",
    # Config
    "model": (
        "Path to a model file. This should be a file that works with"
        " llama.cpp, like gguf files for instance. It can also be a ChatGPT or Gemini model."
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
        "(Only for local models) The Top-k parameter limits the model's"
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
    "search": "Enable the search tool, which means the AI might do web searches to get information. This might incur slower and more expensive responses",
    "stream": "Enable response streaming instead of waiting for the full response",
    "batch_size": "Batch size for prompt processing. Higher values can speed up initial prompt evaluation but use more memory",
    "ubatch_size": "Physical batch size for token generation. Higher values can improve generation speed but use more memory",
    # Find
    "find_next_i": f"Find next match (case insensitive). {middleprev}",
    "find_next": f"Find next match (case sensitive). {middleprev}",
    "find_bound_i": f"Find next word-bound match (case insensitive). {middleprev}",
    "find_bound": f"Find next word-bound match (case sensitive). {middleprev}",
    "find_hide": "Hide the find bar (Esc)",
    # Autoscroll
    "autoscroll_slower": "Decrease autoscroll speed. Middle click for min speed",
    "autoscroll": "Toggle autoscroll. Middle click to reset delay. Right click to autoscroll up",
    "autoscroll_faster": "Increase autoscroll speed. Middle click for max speed",
    # Tabs
    "tabs_left": f"Go to the tab on the left. Middle click to go to the first tab. {tab_btns}",
    "tabs_right": f"Go to the tab on the right. Middle click to go to the last tab. {tab_btns}",
}
