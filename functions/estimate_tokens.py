import tiktoken

def estimate_tokens(text, model_name='gpt-4'):
    """
    Estimates the number of tokens in a text using TikToken.

    Parameters:
    - text (str): The text to estimate token count for.
    - model_name (str): The model to estimate tokens for. Defaults to 'gpt-4'.

    Returns:
    - int: The estimated number of tokens.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(text))
    return num_tokens