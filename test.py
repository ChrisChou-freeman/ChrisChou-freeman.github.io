import random

class Sort(object):
    def __init__(self, length):
        self.the_list = range(length)
        random.shuffle(self.the_list)
        self.length = length
    
    def exchange(self, l, r):
        temp = self.the_list[l]
        self.the_list[l] = self.the_list[r]
        self.the_list[r] = temp

    def pop_sort(self):
        for i in xrange(self.length):
            for j in xrange(i+1, self.length):
                if self.the_list[j] < self.the_list[i]:
                    self.exchange(i, j)
    
    def select_sort(self):
        for i in xrange(self.length):
            small = i
            for j in xrange(i+1, self.length):
                if self.the_list[j] < self.the_list[small]:
                    small = j
            if i != small:
                self.exchange(i, small)
    
    def insert_sort(self):
        for i in xrange(1, self.length):
            pre = i - 1
            current = self.the_list[i]
            while pre >= 0 and self.the_list[pre] > current:
                self.exchange(pre, pre + 1)
                pre -= 1
            
    
    def shell_sort(self):
        sep = self.length//2
        while sep > 0:
            for i in range(sep, self.length):
                pre = i - sep
                current = self.the_list[i]
                while pre >=0 and self.the_list[pre] > current:
                    self.exchange(pre, pre+sep)
                    pre -= sep
            sep = sep//2

    def quick_sort(self, left, right):
        if left >= right:
            return
        flag = left
        for i in range(left+1, right+1):
            if self.the_list[i] < self.the_list[flag]:
                temp = self.the_list[i]
                del self.the_list[i]
                self.the_list.insert(flag, temp)
                flag += 1
        self.quick_sort(left, flag-1)
        self.quick_sort(flag+1, right)

sort  = Sort(15)

sort.quick_sort(0, sort.length-1)
print sort.the_list