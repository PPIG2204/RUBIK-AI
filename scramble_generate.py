import stress_test

if __name__ == "__main__":
    fout = open("scrambles.csv","w")
    for i in range(5000):
        a=stress_test.generate_random_scramble(5)
        print(" ".join(a),file=fout,end=',')
    for i in range(10000):
        a=stress_test.generate_random_scramble(6)
        print(" ".join(a),file=fout,end=',')
    for i in range(20000):
        a=stress_test.generate_random_scramble(7)
        print(" ".join(a),file=fout,end=',')
    for i in range(40000):
        a=stress_test.generate_random_scramble(8)
        print(" ".join(a),file=fout,end=',')
    for i in range(55000):
        a=stress_test.generate_random_scramble(9)
        print(" ".join(a),file=fout,end=',')
    for i in range(60000):
        a=stress_test.generate_random_scramble(10)
        print(" ".join(a),file=fout,end=',')

    fout.close()