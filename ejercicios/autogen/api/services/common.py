def get_humor_instruction(level: int) -> str:
    """
    Generates a system instruction based on the humor level.
    """
    if level <= 2:
        return "You are extremely serious, formal, and professional. Do not use any humor. Be concise and factual."
    elif level <= 5:
        return "You are professional but approachable. You can be slightly casual but keep it business-like."
    elif level <= 8:
        return "You are friendly and witty. Feel free to use light humor and be conversational."
    else:
        return "You are a hilarious comedian. Be extremely funny, informal, and crack jokes in your response. Use emojis."
