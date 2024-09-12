def combinations(letters, spaces):
    if spaces == 0:
        return [""]
    
    result = []
    for i, letter in enumerate(letters):
        remaining_letters = letters[:i] + letters[i+1:]
        for combo in combinations(remaining_letters, spaces - 1):
            result.append(letter + combo)
    
    return result

print(combinations(['a', 'e', 'b', 'd', 'c', 't'], 3))