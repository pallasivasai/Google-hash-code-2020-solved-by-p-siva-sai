
"""
More pizza problem.

3 algorithms to solve the more pizaa problem.
"""
import os


class pizza:
    """Return the maximum possible pizza slices and their formations."""

    def __init__(self, filepath):
        """Initiate bound, types and slices."""
        with open(filepath, "r") as file:
            dat = file.readlines()
            self.bound, self.types = [int(item) for item in dat[0][:-1].split(" ")]
            self.slices = [int(item) for item in dat[1][:-1].split(" ")]

    def MaxPizza(self):
        """BFS - slow."""
        dicti = {0: []}
        for i, s in enumerate(self.slices):
            temp = {}
            for d in dicti:
                cur = s + d
                if cur <= self.bound and cur not in dicti and cur not in temp:
                    temp[cur] = dicti[d] + [i]
            for t in temp:
                dicti[t] = temp[t]
        return [max(dicti), dicti[max(dicti)]]

    def MaxPizza2(self):
        """Knapsack - slow."""
        ans = [[]] + [[] for i in range(self.bound)]
        for i, s in enumerate(self.slices):
            if self.bound == s or (self.bound > s and ans[self.bound - s]):
                return [s, ans[self.bound - s] + [i]]
            for b in range(self.bound - 1, s, -1):
                if not ans[b] and ans[b - s]:
                    ans[b] = ans[b - s] + [i]
            if self.bound >= s and not ans[s]:
                ans[s] = [i]
        for i in range(self.bound, -1, -1):
            if ans[i]:
                return [i, ans[i]]
        return []

    def MaxPizza3(self):
        """
        DFS - lightning-fast.

        Inspired by the repository from
        "https://github.com/senesh-deshan/Google-Hash-Code-2020"
        """
        n, ans = len(self.slices), [0]
        cur, index = [0], n
        while index:
            index -= 1
            for i in range(index, -1, -1):
                if cur[0] + self.slices[i] <= self.bound:
                    cur[0] += self.slices[i]
                    cur.append(i)
            if cur[0] == self.bound:
                return [cur[0], cur[1:][::-1]]
            if cur[0] > ans[0]:
                ans = cur.copy()
            if len(cur) == 1 or (len(cur) == 2 and not cur[-1]):
                break
            if not cur[-1]:
                cur[0] -= self.slices[cur.pop()]
            index = cur.pop()
            cur[0] -= self.slices[index]
        return [ans[0], ans[1:][::-1]]


# os.chdir(path)

for name in ["a_example", "b_small", "c_medium", "d_quite_big", "e_also_big"]:
    ans = pizza(name + ".in").MaxPizza3()
    print("Maximum slices possible for '{}' are {}.".format(name, ans[0]))

    file = open(name + "_ans.in", "w")
    file.write(str(len(ans[1])) + "\n")
    file.write(" ".join(str(a) for a in ans[1]))
    file.close()
