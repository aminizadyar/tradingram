import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import io
import urllib, base64


def temp():
    def nrmz(a):
        return [b / a[0] for b in a]

    def getReg(y):

        x = range(0, len(y))
        x = np.array(x)
        x = x.reshape((-1, 1))
        model = LinearRegression().fit(x, y)
        r_sq = model.score(x, y)
        return r_sq

    def getVar(y):
        x = range(0, len(y))
        x = np.array(x)
        x = x.reshape((-1, 1))
        model = LinearRegression().fit(x, y)
        y_pred = model.predict(x)
        delta = y - y_pred
        n = len(y)
        Var = sum(delta ** 2) / n
        return Var

    def getReturn(y):
        x = range(0, len(y))
        x = np.array(x)
        x = x.reshape((-1, 1))
        model = LinearRegression().fit(x, y)
        x1 = np.array([len(y)]).reshape((-1, 1))
        y1 = model.predict(x1)
        K = (y1 - y[0]) / y[0]
        return K

    def getCorr():

        sandogh1 = int(input("sandogh1 :"))
        sandogh2 = int(input("sandogh2 :"))
        start = int(input("start :"))
        end = int(input("end :"))
        r = np.corrcoef(p_new[sandogh1][start:end], p_new[sandogh2][start:end])

        plt.figure(figsize=(15, 8))
        plt.plot(range(start, end), nrmz(p_new[sandogh1][start:end]))
        plt.plot(range(start, end), nrmz(p_new[sandogh2][start:end]), ls=":")
        plt.grid(ls="dashed")
        plt.title(f"correlation:{r[0, 1]}")
        plt.show()

    def filter(profile):

        for i in range(0, len(profile)):
            s = 0
            if (i > len(profile) - 1):
                i = len(profile) - 1

            for j in range(0, len(profile)):

                if (profile[i][0] < profile[j][0] and profile[i][1] > profile[j][1]):
                    del profile[i]
                    s = 1
                if (s == 1):
                    break

        return profile

    def scaled(a, beta):

        x = [0] * len(a)
        alpha = [0] * len(a)
        for i in range(0, len(a)):
            x[i] = a[i] ** beta
        if (sum(x) > 0):
            for i in range(0, len(a)):
                alpha[i] = x[i] / sum(x)
        if (sum(x) == 0):
            for i in range(0, len(a)):
                alpha[i] = 1 / len(a)

        return alpha

    ETF_list = ["BUG", "QYLD", "LIT", "PAVE"]
    p_new = [0] * len(ETF_list)

    for i in range(0, len(ETF_list)):
        p_new[i] = yf.Ticker(f"{ETF_list[i]}").history(start="2021-03-01", end="2021-08-08")["Close"]

    n_of_data_gathering = [3, 4, 5, 6, 7]
    BETA = [0.002, 0.001, 0.0005, 0.0003, 0.0002, 0.00001, 0.006, 0.01, 0.02, 0.03]
    choices = [(a, b) for a in n_of_data_gathering for b in BETA]

    Ks = []

    uu = [0] * len(choices)

    for y in range(0, len(choices)):

        end = 10  # start engin from
        N = 75

        n = choices[y][0]
        beta = choices[y][1]

        start = end - n

        uu[y] = [0] * (N + 1)
        uu[y][0] = 1
        Vars = [0] * N
        Sigmas = [0] * N
        ExpReturns = [0] * N
        Regression = [0] * N
        profile = [0] * N
        my_portfo = [0] * N
        m_sandogh = [0] * N
        K = [0] * N

        for q in range(0, N):

            Regression[q] = [0] * len(ETF_list)
            Vars[q] = [0] * len(ETF_list)
            Sigmas[q] = [0] * len(ETF_list)
            ExpReturns[q] = [0] * len(ETF_list)
            profile[q] = [0] * len(ETF_list)

            for j in range(0, len(ETF_list)):
                ExpReturns[q][j] = getReturn(p_new[j][q + start:q + end])
                Vars[q][j] = getVar(nrmz(p_new[j][q + start:q + end]))
                Regression[q][j] = getReg(nrmz(p_new[j][q + start:q + end]))
                Sigmas[q][j] = Vars[q][j] ** 0.5
                profile[q][j] = [0] * 2
                profile[q][j][0] = ExpReturns[q][j]
                profile[q][j][1] = Vars[q][j]

            profile[q] = filter(profile[q])

            m_sandogh[q] = []

            for i in range(0, len(ETF_list)):
                for j in range(0, len(profile[q])):
                    if (str(ExpReturns[q][i])[0:8] == str(profile[q][j][0])[0:8] and ExpReturns[q][i] > 0):
                        m_sandogh[q].append(i)

            for i in range(0, len(profile[q])):
                if (q > 0 and ExpReturns[q - 1][i] < 0 and Regression[q][i] < Regression[q - 1][i] and
                        ExpReturns[q - 1][i] < ExpReturns[q][i]):
                    m_sandogh[q].append(i)

            profile_sandogh = []

            for i in m_sandogh[q]:
                profile_sandogh.append([Sigmas[q][i], i])

            profile_sandogh.sort()

            c = 1
            s = 0
            r = 0
            e = 0

            for i in m_sandogh[q]:

                if (q > 0 and i in m_sandogh[q - 1] and Regression[q][i] < 0.65 * Regression[q - 1][i] and
                        ExpReturns[q][i] < ExpReturns[q - 1][i]):
                    for j in range(0, len(profile_sandogh)):
                        if (profile_sandogh[j][1] == i):
                            del profile_sandogh[j]
                            break

            for i in range(0, len(profile_sandogh)):
                e += ExpReturns[q][profile_sandogh[i][1]]

            if (len(m_sandogh[q]) == 0 or e < 0):
                K[q] = 0


            else:

                pre_alpha = [0] * len(profile_sandogh)
                for i in range(0, len(profile_sandogh)):
                    pre_alpha[i] = profile_sandogh[i][0]
                alpha = scaled(pre_alpha, beta)
                K[q] = 0
                for i in range(0, len(profile_sandogh)):
                    K[q] += alpha[i] * (
                                (p_new[profile_sandogh[i][1]][end + q] - p_new[profile_sandogh[i][1]][end + q - 1]) / (
                        p_new[profile_sandogh[i][1]][end + q - 1]))

            uu[y][q + 1] = uu[y][q] * (1 + K[q])

        Ks.append(uu[y][N])

        # figure of best choice

    best_choice = Ks.index(max(Ks))

    plt.figure(figsize=(15, 8))  # end-1 : uu[0] =1     end : uu[1]
    for j in range(0, len(ETF_list)):
        plt.plot(range(end, end + N), nrmz(p_new[j][end:end + N]))  # lw = j/2

    plt.plot(range(end, end + N), nrmz(uu[best_choice][1:N + 1]), ls=":")
    plt.grid(ls="dashed")
    plt.title(f"Optimum Values:   n = {choices[best_choice][0]}  and  beta = {choices[best_choice][1]} ")
    fig = plt.gcf()
    # convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri
