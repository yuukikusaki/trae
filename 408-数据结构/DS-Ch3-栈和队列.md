---
tags: [408, 数据结构, Ch3, 栈, 队列, 表达式求值, 括号匹配, 数组, 矩阵压缩]
aliases: [DS第三章, 栈和队列, 栈队列和数组]
---

# Ch3 栈、队列和数组 —— 受限的线性表，无限的考点

> 🔗 [[DS-MOC-数据结构总览|MOC]] | 上一章：[[DS-Ch2-线性表]] | 下一章：[[DS-Ch4-串]] | [[DS-大题模板]]

---

## 3.1 栈 Stack — LIFO

### 顺序栈实现（408 标准写法）

```c
#include <stdio.h>
#include <stdlib.h>
#define MAXSIZE 100

typedef struct {
    int data[MAXSIZE];
    int top;           // ⭐ 栈顶指针：-1 表示空栈
} SqStack;

//==408考点== 初始化 O(1)
void InitStack(SqStack *S) {
    S->top = -1;       // 也可用 top=0 表示空栈，看题目约定
}

int StackEmpty(SqStack *S) { return S->top == -1; }
int StackFull(SqStack *S)  { return S->top == MAXSIZE - 1; }

//==408考点== 入栈 O(1)
int Push(SqStack *S, int e) {
    if (StackFull(S)) return 0;
    S->data[++(S->top)] = e;  // 先 +1，再放入
    return 1;
}

//==408考点== 出栈 O(1)
int Pop(SqStack *S, int *e) {
    if (StackEmpty(S)) return 0;
    *e = S->data[(S->top)--]; // 先取出，再 -1
    return 1;
}

// 取栈顶（不出栈）O(1)
int GetTop(SqStack *S, int *e) {
    if (StackEmpty(S)) return 0;
    *e = S->data[S->top];
    return 1;
}
```

### 链栈（了解即可，408 很少专门考）

```c
typedef struct SNode {
    int data;
    struct SNode *next;
} SNode, *LinkStack;

// 入栈 = 头插法；出栈 = 删除头结点后的第一个结点
// 时间复杂度均为 O(1)
```

### 🔥 栈的 408 经典应用

```c
//==408考点== 括号匹配
int BracketMatch(char *str) {
    SqStack S; InitStack(&S);
    for (int i = 0; str[i]; i++) {
        if (str[i] == '(' || str[i] == '[' || str[i] == '{')
            Push(&S, str[i]);
        else if (str[i] == ')' || str[i] == ']' || str[i] == '}') {
            if (StackEmpty(&S)) return 0;  // 右括号多了
            char top; Pop(&S, &top);
            if ((str[i] == ')' && top != '(') ||
                (str[i] == ']' && top != '[') ||
                (str[i] == '}' && top != '{'))
                return 0;  // 不匹配
        }
    }
    return StackEmpty(&S);  // 栈空 → 全部匹配
}
```

> ⚠️ 408 大题可能让你**手写**括号匹配，关键点：(1) 左括号入栈 (2) 右括号出栈比对 (3) 结束时栈必须为空。

---

## 3.2 队列 Queue — FIFO

### 循环队列（408 最常考）

```c
#define MAXSIZE 100

typedef struct {
    int data[MAXSIZE];
    int front;  // 队头指针
    int rear;   // 队尾指针（指向队尾元素的下一个位置）
} SqQueue;

//==408考点== 判空判满 — 408 高频选择题陷阱
void InitQueue(SqQueue *Q) {
    Q->front = Q->rear = 0;
}

// 判空：front == rear
// 判满：(rear + 1) % MAXSIZE == front  ← 牺牲一个单元
// 元素个数：(rear - front + MAXSIZE) % MAXSIZE

int EnQueue(SqQueue *Q, int e) {
    if ((Q->rear + 1) % MAXSIZE == Q->front) return 0;  // 满
    Q->data[Q->rear] = e;
    Q->rear = (Q->rear + 1) % MAXSIZE;
    return 1;
}

int DeQueue(SqQueue *Q, int *e) {
    if (Q->front == Q->rear) return 0;  // 空
    *e = Q->data[Q->front];
    Q->front = (Q->front + 1) % MAXSIZE;
    return 1;
}
```

### 🔥 判满的三种方式（408 必考对比）

| 方案 | 判空 | 判满 | 优缺点 |
|------|------|------|--------|
| 牺牲一个单元 | front==rear | (rear+1)%MAXSIZE==front | 最常用 |
| 设 size 计数 | size==0 | size==MAXSIZE | 多一个变量 |
| 设 tag 标记 | front==rear && tag==0 | front==rear && tag==1 | 区分最后一次操作是入/出队 |

### 链队列

```c
typedef struct QNode {
    int data;
    struct QNode *next;
} QNode;

typedef struct {
    QNode *front;  // 队头
    QNode *rear;   // 队尾
} LinkQueue;

//==408考点== 入队 O(1)：尾插法
void EnQueue(LinkQueue *Q, int e) {
    QNode *s = (QNode*)malloc(sizeof(QNode));
    s->data = e; s->next = NULL;
    Q->rear->next = s;
    Q->rear = s;
}

//==408考点== 出队 O(1)：删除头结点后的第一个结点
int DeQueue(LinkQueue *Q, int *e) {
    if (Q->front == Q->rear) return 0;
    QNode *p = Q->front->next;
    *e = p->data;
    Q->front->next = p->next;
    if (Q->rear == p) Q->rear = Q->front;  // ⭐ 最后一个结点
    free(p);
    return 1;
}
```

---

## 3.3 栈和队列的 408 互转大题

```c
//==408考点== 用两个栈实现队列 —— 408 历年真题高频
typedef struct {
    SqStack s1;  // 入队栈
    SqStack s2;  // 出队栈
} MyQueue;

void EnQueue(MyQueue *Q, int e) {
    Push(&Q->s1, e);            // 直接 push 到 s1
}

int DeQueue(MyQueue *Q, int *e) {
    if (StackEmpty(&Q->s2)) {   // s2 空时，把 s1 全部倒入 s2
        int t;
        while (!StackEmpty(&Q->s1)) {
            Pop(&Q->s1, &t);
            Push(&Q->s2, t);    // 倒一次顺序就反了 → 变成 FIFO
        }
    }
    if (StackEmpty(&Q->s2)) return 0;
    Pop(&Q->s2, e);
    return 1;
}
// 均摊 O(1) — 每个元素最多进栈 2 次、出栈 2 次
```

---

## 📝 408 考点速记

| 结构 | 特性 | 408大题热点 |
|------|------|------------|
| 栈 | LIFO | 括号匹配、表达式求值、递归转非递归 |
| 队列 | FIFO | 层序遍历、缓冲区、双栈模拟队列 |
| 循环队列 | 环形数组 | **判空判满条件**（选择题高频） |
| 链栈 | 链表+栈 | 不考大题，了解即可 |

### 🔥 易错点

- ❌ 循环队列 `front==rear` 分不清是空还是满 → ✅ 需额外手段（牺牲单元/size/tag）
- ❌ 链队出队时忘记 `rear` 也要更新（删除最后一个结点时）
- ⚠️ 表达式求值中，操作符栈 + 操作数栈，**优先级比较**是核心

---

## 🔥 教材补充：共享栈（408选择题考点）

两个栈共享一维数组空间，栈底分别在数组两端，栈顶向中间延伸。

```c
#define MAXSIZE 100
typedef struct {
    int data[MAXSIZE];
    int top0;   // 栈0栈顶（从左端开始，初始 -1）
    int top1;   // 栈1栈顶（从右端开始，初始 MAXSIZE）
} ShareStack;

// 栈0入栈
int Push0(ShareStack *S, int e) {
    if (S->top0 + 1 == S->top1) return 0;  // 栈满
    S->data[++(S->top0)] = e;
    return 1;
}

// 栈1入栈
int Push1(ShareStack *S, int e) {
    if (S->top0 + 1 == S->top1) return 0;  // 栈满
    S->data[--(S->top1)] = e;
    return 1;
}
// 判满条件：top0 + 1 == top1
// 优势：空间利用率高，一个栈满时另一个可能还有空间
```

---

## 🔥 教材补充：双端队列（408选择题考点）

**定义**：允许两端都可以进行插入和删除操作的线性表。

| 类型 | 前端操作 | 后端操作 |
|------|----------|----------|
| 输入受限 | 可删除 | 可插入/可删除 |
| 输出受限 | 可插入/可删除 | 可插入 |
| 普通双端 | 可插入/可删除 | 可插入/可删除 |

> **408考点**：双端队列的**输出序列合法性**判断（与栈的Catalan数结合考查）。

---

## 🔥 教材补充：Catalan数与出栈序列

n个不同元素按固定次序入栈时，可能的出栈序列总数为：
$$C_n = \frac{1}{n+1}\binom{2n}{n}$$

| n | 1 | 2 | 3 | 4 | 5 |
|---|:-:|:-:|:-:|:-:|:-:|
| Catalan数 | 1 | 2 | 5 | 14 | 42 |

> **408考点**：2015年真题考查过Catalan数概念。选择题中常给出n=3或4，让你判断某个序列是否**不可能**为出栈序列。

---

## 🔥 教材补充：栈在表达式求值中的应用

### 中缀转后缀（算符优先法）

```c
// 中缀表达式转后缀的栈操作规则
// 1. 操作数直接输出
// 2. 左括号入栈
// 3. 右括号：弹出并输出直到左括号
// 4. 运算符：与栈顶比较优先级，栈顶>=当前则弹出，直到栈顶<当前，然后当前入栈
```

| 运算符 | 优先级 |
|--------|--------|
| ( | 最低（栈内） |
| + - | 1 |
| * / | 2 |

---

## 🎯 力扣推荐

| 题目 | 难度 | 推荐理由 | 408考点关联 |
|------|------|----------|------------|
| [20. 有效的括号](https://leetcode.cn/problems/valid-parentheses/) | 简单 | 栈的最经典应用 | 408括号匹配大题标准题 |
| [155. 最小栈](https://leetcode.cn/problems/min-stack/) | 中等 | 辅助栈思维 | 408中栈的灵活应用 |
| [232. 用栈实现队列](https://leetcode.cn/problems/implement-queue-using-stacks/) | 简单 | 双栈模拟 | ⭐ 408高频大题（笔记中已实现） |
| [225. 用队列实现栈](https://leetcode.cn/problems/implement-stack-using-queues/) | 简单 | 双队列模拟 | 与232相对的考点 |
| [150. 逆波兰表达式求值](https://leetcode.cn/problems/evaluate-reverse-polish-notation/) | 中等 | 后缀表达式求值 | 408表达式求值核心考点 |
| [239. 滑动窗口最大值](https://leetcode.cn/problems/sliding-window-maximum/) | 困难 | 单调队列 | 408不直接考，扩展思路 |
| [739. 每日温度](https://leetcode.cn/problems/daily-temperatures/) | 中等 | 单调栈 | 栈的进阶应用 |

> 💡 **刷题建议**：20、232、150 三题必做。20直接对应408括号匹配大题；232对应408双栈模拟队列真题；150对应表达式求值。

---

## 🔥 408与力扣的差异

| 方面 | 力扣 | 408 |
|------|------|-----|
| 栈的Top值 | 习惯 top=0 表示空 | 常用 top=-1（本笔记） |
| 队列判满 | 通常用动态数组 | 循环队列牺牲单元法最常考 |
| 空间限制 | 宽裕 | O(1) 辅助空间是经典要求 |

---

## 📖 教材补充：数组与特殊矩阵的压缩存储（408选择题高频）

> 教材第3章包含**数组**部分，这是现有笔记缺失的重要内容。

### 一维数组的存储

一维数组 A[n] 的存储地址：
- `LOC(i) = LOC(0) + i x L`，其中 L 为每个元素所占存储单元

### 多维数组的存储

二维数组 A[m][n]：
- **行优先**：`LOC(i,j) = LOC(0,0) + (i x n + j) x L`
- **列优先**：`LOC(i,j) = LOC(0,0) + (j x m + i) x L`

### 对称矩阵的压缩存储

对称矩阵 A[n][n] 中 `A[i][j] = A[j][i]`，只需存储下三角（含对角线）：
- 元素个数：n(n+1)/2
- 一维数组 B[k] 中，`k = i(i+1)/2 + j`（下三角，i>=j）
- **408选择题常考**：给定 (i,j)，求压缩后的数组下标

### 三角矩阵

- **下三角矩阵**：`k = i(i+1)/2 + j`（i>=j），最后一个位置存常数c
- **上三角矩阵**：`k = j(j+1)/2 + i`（j>=i），最后一个位置存常数c

### 三对角矩阵（带状矩阵）

- 非零元素在三条对角线上：`|i-j| <= 1`
- 非零元素个数：3n-2
- 压缩到 B[3n-2]：`k = 2i + j - 3`（从0开始且i,j从1开始）
- **408常考**：给定位置 (i,j) 求 B[k] 中的下标，或反向求

### 稀疏矩阵的存储

- **三元组法**：`(i, j, A[i][j])` 的集合
- **十字链表法**：每行每列带头结点的链表
- **408考点**：稀疏矩阵的压缩存储不丢失信息（三元组可还原），但失去随机存取特性

```
// 三元组示例
typedef struct {
    int row, col;  // 非零元素的行号和列号
    int value;     // 非零元素的值
} Triple;

typedef struct {
    Triple data[MAXSIZE];  // 三元组表
    int rows, cols, num;   // 矩阵行数、列数、非零元素个数
} TSMatrix;
```

> ⚡ **408常考公式**：对称矩阵 A[i][j]（i>=j）压缩到 B[k]，`k = i(i-1)/2 + j - 1`（i,j从1开始）。注意起始下标是0还是1！

---

> 🔗 上一章：[[DS-Ch2-线性表]] | 下一章：[[DS-Ch4-串]] | [[DS-大题模板]]
