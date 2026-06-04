---
tags: [408, 数据结构, Ch4, 串, KMP]
aliases: [DS第四章]
---

# 第4章 串

> [[DS-MOC-数据结构总览|MOC]]
> 上一章：[[DS-Ch3-栈和队列]] | 下一章：[[DS-Ch5-树与二叉树]]

---

## 4.1 串的基本概念

串（String）是由零个或多个字符组成的有限序列，一般记为：

$$S = 'a_1a_2 \dots a_n' \quad (n \ge 0)$$

| 术语 | 含义 |
|------|------|
| 串名 | S |
| 串值 | 用单引号括起来的字符序列 |
| 串长 | 串中字符个数 n，n=0 时称为**空串** |
| 子串 | 串中任意连续字符组成的子序列 |
| 主串 | 包含子串的串 |
| 位置 | 字符在串中的序号（408 中从 1 开始） |

> **408 注意**：空串 `""` 与空格串 `" "` 不同——前者长度为 0，后者由一个空格字符组成，长度为 1。

---

## 4.2 串的存储结构

### 4.2.1 定长顺序存储（408 只考这种）

```c
//==408考点== 定长顺序存储——408唯一考察的串存储方式
#define MAXLEN 255   // 预定义最大串长

typedef struct {
    char ch[MAXLEN]; // 每个分量存储一个字符，408中下标从1开始
    int  length;     // 串的实际长度
} SString;
```

> **408 关键约定**：串的数组下标**从 1 开始**（ch[0] 闲置不用），这与普通 C 编程不同，但 408 教材和考题都遵循此约定。**模式匹配时下标一律从 1 开始编号**。

### 4.2.2 其他存储方式（408 不考，仅作了解）

- **堆分配存储**：动态分配连续存储空间（`char*` + `malloc`）
- **块链存储**：用链表存储串，每个结点存多个字符

---

## 4.3 朴素模式匹配算法

### 4.3.1 算法思想

主串 S 长度为 n，模式串 T 长度为 m。从 S 的第 1 个字符开始，逐个与 T 比较；若匹配失败，S 回到 **i - j + 2**（下一趟起始位置），T 回到第 1 个字符（j = 1）。

### 4.3.2 完整 C 代码

```c
#include <stdio.h>
#include <string.h>

#define MAXLEN 255

typedef struct {
    char ch[MAXLEN];
    int  length;
} SString;

//==408考点== 朴素模式匹配：最坏 O(mn)，会反复回溯
int Index_BF(SString S, SString T) {
    int i = 1, j = 1; // 408约定：下标从1开始
    while (i <= S.length && j <= T.length) {
        if (S.ch[i] == T.ch[j]) {
            i++; j++;        // 当前字符匹配，继续比较后继
        } else {
            i = i - j + 2;   //==408考点== 指针回溯：i回到下一趟的起始位置
            j = 1;           //==408考点== j回到模式串首位置
        }
    }
    if (j > T.length)
        return i - T.length; // 匹配成功，返回首字符位置
    else
        return 0;            // 408中返回0表示匹配失败
}

// 辅助函数：将C字符串转为SString（下标从1开始）
void StrAssign(SString *S, const char *src) {
    int len = strlen(src);
    S->length = len;
    for (int i = 1; i <= len; i++)
        S->ch[i] = src[i - 1];
}

int main() {
    SString S, T;
    StrAssign(&S, "ababcabcacbab");
    StrAssign(&T, "abcac");

    int pos = Index_BF(S, T);
    printf("匹配位置: %d\n", pos); // 输出: 6
    return 0;
}
```

### 4.3.3 时间复杂度分析

- 最坏情况：每趟比较到 T 的最后一个字符才发现不匹配，如 `S = "aaaaaaaaab"`, `T = "aaab"`
- 比较趟数：n - m + 1 趟，每趟比较 m 次
- 最坏复杂度：**O(mn)**

---

## 4.4 KMP 算法（408 大题必考）

### 4.4.1 为什么需要 KMP

朴素匹配的问题：主串指针 i 的回溯是多余的。KMP 的核心思想是——**利用已经部分匹配的信息，让 i 不回溯，只移动 j**。

当 `S.ch[i] != T.ch[j]` 时，j 不是无脑回到 1，而是回到 `next[j]`。

```c
i = i;          //==408考点== 主串指针i保持不动！
j = next[j];    //==408考点== 模式串j跳到next[j]位置
```

### 4.4.2 Next 数组的手工求法（408 大题核心考点）

next 数组的含义：**当模式串第 j 个字符失配时，j 应该跳回的位置。**

#### 手算三步法（考试用这个方法）

> **第 1 步**：写出模式串，编号 j = 1, 2, 3, ..., m

> **第 2 步**：对每个 j，观察 `T[1 .. j-1]`（即前 j-1 个字符构成的子串），找出其**最长的相等前后缀长度**，记为 k

> **第 3 步**：`next[j] = k + 1`（特殊情况 next[1] = 0，next[2] = 1）

**手算实例**：模式串 T = "abcac"

| j | 1 | 2 | 3 | 4 | 5 |
|:-:|:-:|:-:|:-:|:-:|:-:|
| T[j] | a | b | c | a | c |
| 前j-1个字符 | - | "a" | "ab" | "abc" | "abca" |
| 最长相等前后缀 | - | 无 | 无 | 无 | "a" (长1) |
| next[j] | **0** | **1** | **1** | **1** | **2** |

详细过程：
- j=1：next[1] 恒为 **0**（特殊规定）
- j=2：前 1 个字符 "a"，无前后缀，next[2] = **1**
- j=3：前 2 个字符 "ab"：前缀 {"a"}，后缀 {"b"}，无相等 → next[3] = **1**
- j=4：前 3 个字符 "abc"：前缀 {"a","ab"}，后缀 {"c","bc"}，无相等 → next[4] = **1**
- j=5：前 4 个字符 "abca"：前缀 {"a","ab","abc"}，后缀 {"a","ca","bca"}，相等 "a" 长度 1 → next[5] = **2**

**另一个常考实例**：T = "abaabc"

| j | 1 | 2 | 3 | 4 | 5 | 6 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| T[j] | a | b | a | a | b | c |
| next[j] | 0 | 1 | 1 | 2 | 2 | 3 |

**推导**（重点理解 j=4 和 j=5）：
- j=4：前 3 个字符 "aba"：前缀 {"a","ab"}，后缀 {"a","ba"}，相等 "a" 长 1 → next[4] = 2
- j=5：前 4 个字符 "abaa"：前缀 {"a","ab","aba"}，后缀 {"a","aa","baa"}，相等 "a" 长 1 → next[5] = 2
- j=6：前 5 个字符 "abaab"：前缀 {"a","ab","aba","abaa"}，后缀 {"b","ab","aab","baab"}，相等 "ab" 长 2 → next[6] = 3

### 4.4.3 Next 数组的编程求解

```c
//==408考点== 求next数组：时间复杂度 O(m)
void get_next(SString T, int next[]) {
    int j = 1, k = 0;
    next[1] = 0; //==408考点== next[1]恒为0，是特殊标志
    while (j < T.length) {
        if (k == 0 || T.ch[j] == T.ch[k]) {
            j++; k++;
            next[j] = k; //==408考点== next[j+1] = k+1
        } else {
            k = next[k]; //==408考点== 失配时用next回溯k（自己匹配自己）
        }
    }
}
```

### 4.4.4 KMP 完整代码

```c
#include <stdio.h>
#include <string.h>

#define MAXLEN 255

typedef struct {
    char ch[MAXLEN];
    int  length;
} SString;

//==408考点== 求next数组 O(m)
void get_next(SString T, int next[]) {
    int j = 1, k = 0;
    next[1] = 0;
    while (j < T.length) {
        if (k == 0 || T.ch[j] == T.ch[k]) {
            j++; k++;
            next[j] = k;
        } else {
            k = next[k];
        }
    }
}

//==408考点== KMP主算法：O(n)，主串指针i绝不回溯
int Index_KMP(SString S, SString T, int next[]) {
    int i = 1, j = 1;
    while (i <= S.length && j <= T.length) {
        if (j == 0 || S.ch[i] == T.ch[j]) {
            //==408考点== j==0表示比较应从模式串第1个字符重新开始
            i++; j++;
        } else {
            j = next[j]; //==408考点== 仅j回溯，i不动
        }
    }
    if (j > T.length)
        return i - T.length;
    else
        return 0;
}

void StrAssign(SString *S, const char *src) {
    int len = strlen(src);
    S->length = len;
    for (int i = 1; i <= len; i++)
        S->ch[i] = src[i - 1];
}

int main() {
    SString S, T;
    StrAssign(&S, "ababcabcacbab");
    StrAssign(&T, "abcac");

    int next[MAXLEN];
    get_next(T, next);

    printf("next数组: ");
    for (int i = 1; i <= T.length; i++)
        printf("%d ", next[i]);
    printf("\n"); // 输出: 0 1 1 1 2

    int pos = Index_KMP(S, T, next);
    printf("匹配位置: %d\n", pos); // 输出: 6
    return 0;
}
```

---

## 4.5 Nextval 数组（KMP 的进一步优化）

### 4.5.1 为什么需要 nextval

当 `T.ch[j] == T.ch[next[j]]` 时，用 next[j] 会做一次**无意义的比较**（明知不等还去比较），需要进一步优化。

### 4.5.2 Nextval 的手算方法

从 j=1 开始依次推导：

> 规则：如果 `T.ch[nextval[j]] == T.ch[j]`，则 `nextval[j] = nextval[nextval[j]]`；否则 `nextval[j] = next[j]`

**实例**：T = "aaaab"（这个例子最能体现优化效果）

| j | 1 | 2 | 3 | 4 | 5 |
|:-:|:-:|:-:|:-:|:-:|:-:|
| T[j] | a | a | a | a | b |
| next[j] | 0 | 1 | 2 | 3 | 4 |
| nextval[j] | **0** | **0** | **0** | **0** | **4** |

推导过程：
- nextval[1] = **0**（恒为 0）
- j=2：next[2]=1，T[1]='a' == T[2]='a'，继承：nextval[2] = nextval[1] = **0**
- j=3：next[3]=2，T[2]='a' == T[3]='a'，继承：nextval[3] = nextval[2] = **0**
- j=4：next[4]=3，T[3]='a' == T[4]='a'，继承：nextval[4] = nextval[3] = **0**
- j=5：next[5]=4，T[4]='a' != T[5]='b'，保持：nextval[5] = next[5] = **4**

> **对比效果**：用 next 时，T = "aaaab" 失配后 j 从 4 一路退到 1（4 次回溯）；用 nextval 直接退到 0（1 步到位），**大幅减少比较次数**。

**另一个实例**：T = "abcac"

| j | 1 | 2 | 3 | 4 | 5 |
|:-:|:-:|:-:|:-:|:-:|:-:|
| T[j] | a | b | c | a | c |
| next[j] | 0 | 1 | 1 | 1 | 2 |
| nextval[j] | **0** | **1** | **1** | **0** | **1** |

推导过程：
- nextval[1] = **0**
- j=2：next[2]=1，T[1]='a' != T[2]='b'，nextval[2] = next[2] = **1**
- j=3：next[3]=1，T[1]='a' != T[3]='c'，nextval[3] = next[3] = **1**
- j=4：next[4]=1，T[1]='a' == T[4]='a'，nextval[4] = nextval[1] = **0**
- j=5：next[5]=2，T[2]='b' != T[5]='c'，nextval[5] = next[5] = **2**

### 4.5.3 Nextval 数组的编程求解

```c
//==408考点== 求nextval数组：在求next的同时做优化
void get_nextval(SString T, int nextval[]) {
    int j = 1, k = 0;
    nextval[1] = 0;
    while (j < T.length) {
        if (k == 0 || T.ch[j] == T.ch[k]) {
            j++; k++;
            //==408考点== 关键区别：多一步判断
            if (T.ch[j] != T.ch[k])
                nextval[j] = k;
            else
                nextval[j] = nextval[k]; // 相同则继承
        } else {
            k = nextval[k];
        }
    }
}
```

### 4.5.4 Next 与 Nextval 的区别总结

| 对比项 | next | nextval |
|--------|------|---------|
| 本质 | 最长相等前后缀长度 + 1 | next 的修正版本 |
| 优化场景 | 一般情况 | `T[j] == T[next[j]]` 时避免重复比较 |
| 手算复杂度 | 简单 | 需先算出 next 再逐位修正 |
| 匹配效率 | 好 | **更优**（无多余比较） |
| KMP 时间复杂度 | O(m+n) | O(m+n)，常数因子更小 |

---

## 4.6 KMP 时间复杂度分析

| 阶段 | 操作 | 复杂度 |
|------|------|--------|
| 求 next 数组 | while 循环中 j 每次至少 +1，k 回溯次数受 j 限制 | O(m) |
| 模式匹配 | while 循环中 i 每次至少 +1，j 回溯次数受 i 限制 | O(n) |
| **总计** | | **O(m+n)** |

> **408 记法**：预处理 O(m)，匹配 O(n)，总计 O(m+n)。
>
> 对比朴素匹配最坏 O(mn)，KMP 在 m 和 n 都较大时有显著优势。

---

## 4.7 408 易错点总结

### 4.7.1 下标陷阱

- **408 串的下标一律从 1 开始**，ch[0] 闲置不用
- next[1] 恒为 **0**（不是 -1！注意和某些教材的区别）
- 匹配失败返回 **0**（不是 -1）
- next 数组中 0 的含义："j 退到 0，下一轮 i 和 j 都 +1"

### 4.7.2 Next 数组计算易错

- **next[2] 恒为 1**（无论 T[1] 和 T[2] 是什么字符）
- 求前后缀时只看**真前缀**和**真后缀**（不包含整个子串本身）
- 前后缀比较是从**左到右**看字符是否相同，不是回文
- 当有多个相等前后缀时，取**最长**的那个

### 4.7.3 Nextval 易错

- nextval[1] = **0**（恒为 0）
- 修正规则：比较的是 `T.ch[next[j]]` 和 `T.ch[j]`，不是 `T.ch[nextval[j]]` 和 `T.ch[j]`
- 相等时**递推**：`nextval[j] = nextval[next[j]]`（可能间接跳更多步）

### 4.7.4 常见"坑"

1. **KMP 不一定比朴素快**：如果主串和模式串字符集很小且几乎没有部分匹配（如二进制串），next 数组的作用有限，KMP 常数更大反而可能更慢。
2. **nextval 可能退为 0**：当模式串全为相同字符时（如 "aaaa"），nextval 全为 0 0 0 0，匹配过程几乎一滑到底。
3. **字符串下标从 1 开始的代码不能直接用 C 标准库**：`strlen`、`strcmp` 等都从 0 开始。

---

## 4.8 KMP 匹配过程追踪（帮助理解）

以主串 S = "ababcabcacbab"，模式串 T = "abcac" 为例：

```
next = [0, 1, 1, 1, 2]  （下标1~5）

第1趟: i=1, j=1 → a==a ✓
       i=2, j=2 → b==b ✓
       i=3, j=3 → a!=c ✗ → j=next[3]=1
第2趟: i=3, j=1 → a==a ✓
       i=4, j=2 → b!=b ✗ → j=next[2]=1
第3趟: i=4, j=1 → b!=a ✗ → j=next[1]=0 → i++,j++（特殊处理）
第4趟: i=5, j=1 → c!=a ✗ → j=next[1]=0 → i++,j++
第5趟: i=6, j=1 → a==a ✓
       i=7, j=2 → b==b ✓
       i=8, j=3 → c==c ✓
       i=9, j=4 → a==a ✓
       i=10,j=5 → c==c ✓ → j=6 > 5 → 匹配成功，位置=6
```

> 注意朴素匹配中 i 会反复回溯，而 KMP 中 i 一路向前（从 1 到 10），从未后退。

---

[[DS-MOC-数据结构总览|MOC]]
上一章：[[DS-Ch3-栈和队列]] | 下一章：[[DS-Ch5-树与二叉树]]
