"""The algorithm is designed for the 2020 Hash Code Competition."""
import os


class books:
    """Return the maximum possible scores of books."""

    def __init__(self, filepath):
        """Initiate books, libraries, days, scores, libraBook."""
        with open(filepath, "r") as file:
            dat = file.readlines()
            self.books, self.libraries, self.days = \
                [int(item) for item in dat[0][:-1].split(" ")]
            self.scores = [int(item) for item in dat[1][:-1].split(" ")]
            self.libraBook = []
            for i in range(2, len(dat), 2):
                if dat[i] == "\n":
                    break
                self.libraBook.append(
                    [[int(item) for item in dat[i][:-1].split(" ")],
                     sorted([int(item) for item in dat[i + 1][:-1].split(" ")],
                            key=lambda x: self.scores[x])])
                self.libraBook[-1][0].append(
                    sum(self.scores[b] for b in self.libraBook[-1][1]))
            self.minSignup = min(x[0][1] for x in self.libraBook)

    def bestLib(self, library, left):
        """Select the best libraries for our own solution."""
        if not library or not left:
            return []
        select = [self.libraries + 1, 0, 0]
        for l in library:
            cur = [0, self.libraBook[l][0][3]]
            if self.minSignup + self.libraBook[l][0][1] + 2 <= left:
                index = self.libraBook[l][0][0] - self.libraBook[l][0][2] *\
                    (left - self.minSignup - self.libraBook[l][0][1]) - 2
                for i in range(self.minSignup * self.libraBook[l][0][2]):
                    if index < 0:
                        break
                    cur[0] += self.scores[self.libraBook[l][1][index]]
                    index -= 1
            if cur[0] > select[1] or (
                    cur[0] == select[2] and cur[1] > select[2]):
                select = [l] + cur
        return [select[0]] if select[0] != self.libraries + 1 else []

    def selectBook(self):
        """First solution to select books based on self.bestLib."""
        day, visited, library,  left, select = [
            0], set(), {l for l in range(self.libraries)}, self.days, []
        while True:
            cur = self.bestLib(library, left)
            if not cur:
                break
            select.extend(cur)
            library -= {cur[0]}
            left -= self.libraBook[cur[0]][0][1]
        ans, total = [len(select)], 0
        for s in select:
            day[0] += self.libraBook[s][0][1]
            day.append(self.days - day[0])
        for s, d in zip(select, day[1:]):
            ans.extend([[s], []])
            temp, temp2 = self.libraBook[s][0][2], self.libraBook[s][1][-1]
            while d and self.libraBook[s][1]:
                if not temp:
                    d -= 1
                    temp = self.libraBook[s][0][2]
                else:
                    temp -= 1
                    while self.libraBook[s][1] and \
                            self.libraBook[s][1][-1] in visited:
                        self.libraBook[s][1].pop()
                    if self.libraBook[s][1]:
                        ans[-1].append(self.libraBook[s][1].pop())
                        visited.add(ans[-1][-1])
                        total += self.scores[ans[-1][-1]]
            if not ans[-1]:
                ans[-1].append(temp2)
            ans[-2].append(len(ans[-1]))
        return [total] + ans

    def selectBook2(self):
        """Second solution based on DominikLindorfer's idea in GitHub."""
        visited, ans, signDay, visitedLib = set(), [0, 0], 0, set()
        while True:
            best = [0, -1, 0, []]
            for i, item in enumerate(self.libraBook):
                if i not in visitedLib:
                    item[1] = [j for j in item[1] if j not in visited]
                    if item[0][1] + signDay < self.days and item[1]:
                        temp = sum(self.scores[j] for j in item[1][
                                   -item[0][2] * (
                                       self.days - signDay - item[0][1]):])
                        if temp / item[0][1] > best[2]:
                            best = [temp, i, temp / item[0][1],
                                    item[1][-item[0][2] * (
                                        self.days - signDay - item[0][1]):]]
            if not best[3]:
                break
            signDay += self.libraBook[best[1]][0][1]
            visited |= set(best[3])
            visitedLib.add(best[1])
            ans.extend([[best[1], len(best[3])], best[3]])
            ans[0] += best[0]
            ans[1] += 1
        return ans


# os.chdir(path)
for name in ["a_example", "b_read_on", "c_incunabula",
             "d_tough_choices", "e_so_many_books", "f_libraries_of_the_world"]:
    ans = books(name + ".txt").selectBook2()
    print(ans[0])
    file = open(name + "_ans.txt", "w")
    file.write(str(ans[1]) + "\n")
    for a in ans[2:]:
        file.write(" ".join(str(A) for A in a) + "\n")
    file.close()
