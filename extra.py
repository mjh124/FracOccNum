# Main funtion from mis-implementation of ef_optimizer.py

if __name__ == "__main__":

    # Read orbital energy levels
    MO_en = read_MO_file(fMO)

    # Initialize fermi level guesses
    ef_left = min(MO_en)
    ef_right = max(MO_en)
    ef_mid = (ef_left + ef_right)/2
    efs = [ef_left, ef_right, ef_mid]
    print efs

    thres = 1e3
    for _ in range(100):
        error = [0.0 for i in range(len(efs))]
        for i in range(len(efs)):
            err = fd_2_err(MO_en, efs[i], T)
            error[i] = err
        print error

        left_diff = abs(error[0] - error[2])
        right_diff = abs(error[1] - error[2])
        print "l = ", left_diff
        print "r = ", right_diff

        # Use left half
        if left_diff < right_diff:
            efs[1] = efs[2]
            efs[2] = (efs[0] + efs[2])/2

        # Use right half
        elif left_diff > right_diff:
            efs[0] = efs[2]
            efs[2] = (efs[1] + efs[2])/2

        # If stuck, move the center position a random distance
        elif left_diff == right_diff:
            r = random.uniform(0.25, 0.75)
            efs[2] = (r*efs[0] + (1-r)*efs[1])

        print " ", efs

    fi_final = fermi_dirac(MO_en, efs[i], T)
    print fi_final, np.sum(fi_final)
