def steering_decision(left_detected, right_detected):
    if left_detected and right_detected:
        return "GO STRAIGHT"
    elif left_detected:
        return "TURN RIGHT"
    elif right_detected:
        return "TURN LEFT"
    else:
        return "STOP"
