async def custom_round(self, number: float) -> int:
    """
    Not 'banking' round
    custom_round(3.5) = 4 != round(3.5) = 4
    custom_round(4.5) = 5 != round(4.5) = 4
    """
    if number % 1 < 0.5:
        return int(number)
    else:
        return int(number) + 1
