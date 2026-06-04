---
tags: [408, 数据结构, Ch3, 栈, 队列, 表达式求值, 括号匹配]
aliases: [DS第三章, 栈和队列]
---

# Ch3 栈和队列 —— 受限的线性表，无限的考点

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

//==408考点== 判空判满 — 408 高频选择题陷!!
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

> 🔗 上一章：[[DS-Ch2-线性表]] | 下一章：[[DS-Ch4-串]] | [[DS-大题模板]]
