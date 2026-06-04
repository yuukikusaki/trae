---
tags: [408, 数据结构, Ch2, 线性表, 顺序表, 链表]
aliases: [DS第二章, 线性表]
---

# Ch2 线性表 —— 顺序表 vs 链表，一切数据结构之母

> 🔗 [[DS-MOC-数据结构总览|MOC]] | 上一章：[[DS-Ch1-绪论]] | 下一章：[[DS-Ch3-栈和队列]] | [[DS-大题模板]]

---

## 2.1 顺序表 SeqList — 数组封装的学问

### 完整实现：动态顺序表

```c
#include <stdio.h>
#include <stdlib.h>
#define INIT_SIZE 100
#define INCREMENT 10

typedef struct {
    int *elem;      // 基地址
    int length;     // 当前长度
    int capacity;   // 当前容量
} SeqList;

//==408考点== 初始化 O(1)
void InitList(SeqList *L) {
    L->elem = (int*)malloc(INIT_SIZE * sizeof(int));
    L->length = 0;
    L->capacity = INIT_SIZE;
}

//==408考点== 插入：平均移动 n/2 个 → O(n)
int ListInsert(SeqList *L, int i, int e) {
    // i 是位序（1-based），合法范围 1 ~ length+1
    if (i < 1 || i > L->length + 1) return 0;
    if (L->length >= L->capacity) {
        L->elem = (int*)realloc(L->elem,
            (L->capacity + INCREMENT) * sizeof(int));
        L->capacity += INCREMENT;
    }
    for (int j = L->length; j >= i; j--)
        L->elem[j] = L->elem[j - 1];  // 后移
    L->elem[i - 1] = e;
    L->length++;
    return 1;
}

//==408考点== 删除：也是 O(n)，平均移动 (n-1)/2 个
int ListDelete(SeqList *L, int i, int *e) {
    if (i < 1 || i > L->length) return 0;
    *e = L->elem[i - 1];
    for (int j = i; j < L->length; j++)
        L->elem[j - 1] = L->elem[j];  // 前移
    L->length--;
    return 1;
}

//==408考点== 按值查找 O(n)，按位查找 O(1)
int LocateElem(SeqList *L, int e) {
    for (int i = 0; i < L->length; i++)
        if (L->elem[i] == e) return i + 1;  // 返回位序
    return 0;
}

//==408考点== 逆置 O(n) 原地，空间 O(1) — 408 大题模板题
void Reverse(SeqList *L) {
    int i = 0, j = L->length - 1;
    while (i < j) {
        int t = L->elem[i];
        L->elem[i] = L->elem[j];
        L->elem[j] = t;
        i++; j--;
    }
}

//==408考点== 删除所有值为 x 的元素 O(n)，空间 O(1)
// 核心技巧：双指针（k 记录有效位置）
void DeleteAllX(SeqList *L, int x) {
    int k = 0;  // k 指向下一个有效位置
    for (int i = 0; i < L->length; i++)
        if (L->elem[i] != x)
            L->elem[k++] = L->elem[i];
    L->length = k;
}
```

### 🔥 顺序表 408 考点速记

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| 按位查找 | **O(1)** | 随机存取，最大优势 |
| 按值查找 | **O(n)** | 需遍历 |
| 插入 | **O(n)** | 平均移动 n/2 个元素 |
| 删除 | **O(n)** | 平均移动 (n-1)/2 个元素 |
| 判空 | O(1) | — |

> ⚠️ 插入/删除位置 i 是**位序(1-based)**，对应下标 i-1。408 代码题中位序和下标混用是高频陷阱。

---

## 2.2 单链表 LinkedList — 指针的艺术

### 结点定义 + 头插法/尾插法建表

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct LNode {
    int data;
    struct LNode *next;
} LNode, *LinkList;  // LinkList = LNode*

//==408考点== 头插法建表 O(n)，结果与输入顺序相反
LinkList CreateHead(int a[], int n) {
    LinkList L = (LinkList)malloc(sizeof(LNode));
    L->next = NULL;
    for (int i = 0; i < n; i++) {
        LNode *s = (LNode*)malloc(sizeof(LNode));
        s->data = a[i];
        s->next = L->next;
        L->next = s;     // ⭐ 关键：新结点始终插在头结点之后
    }
    return L;
}

//==408考点== 尾插法建表 O(n)，保持输入顺序
LinkList CreateTail(int a[], int n) {
    LinkList L = (LinkList)malloc(sizeof(LNode));
    L->next = NULL;
    LNode *r = L;  // r 始终指向尾结点
    for (int i = 0; i < n; i++) {
        LNode *s = (LNode*)malloc(sizeof(LNode));
        s->data = a[i];
        r->next = s;
        r = s;           // ⭐ 尾指针后移
    }
    r->next = NULL;
    return L;
}
```

### 核心操作：插入、删除、查找

```c
//==408考点== 按位序插入 O(n)
// 在第 i 个位置插入（1-based）
int ListInsert(LinkList L, int i, int e) {
    LNode *p = L;
    int j = 0;
    while (p && j < i - 1) {  // 找到第 i-1 个结点
        p = p->next;
        j++;
    }
    if (!p || j > i - 1) return 0;  // i 不合法
    LNode *s = (LNode*)malloc(sizeof(LNode));
    s->data = e;
    s->next = p->next;
    p->next = s;
    return 1;
}

//==408考点== 删除结点 O(n)（找前驱）
// ⭐408技巧：若已知要删除结点指针 p，可「偷梁换柱」
// 把 p->next 的值复制到 p，然后删除 p->next（O(1)）
int DeleteNode(LinkList L, int i, int *e) {
    LNode *p = L;
    int j = 0;
    while (p->next && j < i - 1) {
        p = p->next; j++;
    }
    if (!(p->next) || j > i - 1) return 0;
    LNode *q = p->next;
    *e = q->data;
    p->next = q->next;
    free(q);
    return 1;
}

//==408考点== 按值查找 O(n)
LNode* LocateElem(LinkList L, int e) {
    LNode *p = L->next;
    while (p && p->data != e) p = p->next;
    return p;  // 找不到返回 NULL
}
```

### 408 大题高频：链表原地逆置

```c
//==408考点== 原地逆置 O(n), 空间 O(1)
// 经典三指针法：pre, cur, next
void Reverse(LinkList L) {
    LNode *pre = NULL;
    LNode *cur = L->next;
    while (cur) {
        LNode *next = cur->next;  // 先保存后继
        cur->next = pre;          // 反转箭头
        pre = cur;
        cur = next;
    }
    L->next = pre;  // 头结点指向新的首结点
}
```

---

## 2.3 顺序表 vs 链表：408 必考对比

| 对比维度 | 顺序表 | 链表 |
|----------|--------|------|
| 存取方式 | **随机存取** O(1) | **顺序存取** O(n) |
| 插入/删除 | O(n)（需要移动） | O(n)（找前驱）+ O(1)（改指针） |
| 空间 | 预分配，可能浪费 | 动态分配，但有指针开销 |
| 缓存友好 | ✅ 连续存储，空间局部性好 | ❌ 结点分散 |
| 按值查找 | O(n) | O(n) |

> 🔥 408 套路题：给定特定场景（频繁插入删除 vs 频繁查找），选顺序表还是链表？

---

## 📝 408 真题风格代码练习

```c
// 练习1：删除单链表中所有值为 x 的结点（递归写法）
void DeleteX(LinkList L, int x) {
    if (!L) return;
    if (L->data == x) {
        LNode *q = L;
        L = L->next;
        free(q);
        DeleteX(L, x);
    } else {
        DeleteX(L->next, x);
    }
}

// 练习2：归并两个递增有序链表为递减有序
// 思路：头插法 + 两路归并 —— O(m+n)
LinkList MergeDesc(LinkList A, LinkList B) {
    LinkList C = (LinkList)malloc(sizeof(LNode));
    C->next = NULL;
    LNode *pa = A->next, *pb = B->next, *q;
    while (pa && pb) {
        if (pa->data <= pb->data) {
            q = pa; pa = pa->next;
        } else {
            q = pb; pb = pb->next;
        }
        q->next = C->next;  // 头插法 → 自然递减
        C->next = q;
    }
    // 处理剩余部分
    while (pa) { q = pa; pa = pa->next; q->next = C->next; C->next = q; }
    while (pb) { q = pb; pb = pb->next; q->next = C->next; C->next = q; }
    return C;
}
```

---

> 🔗 上一章：[[DS-Ch1-绪论]] | 下一章：[[DS-Ch3-栈和队列]] | [[DS-大题模板]]

---

## 🎯 力扣推荐（核心必刷）

> 💡 你有编程基础，这些题不要只"做一遍"，而是每道题用**2-3种写法**实现，对比408考点与工程实现的差异。

| 题目 | 难度 | 推荐理由 | 408考点关联 |
|------|------|----------|------------|
| [206. 反转链表](https://leetcode.cn/problems/reverse-linked-list/) | 简单 | 408最高频大题模板 | 三指针逆置（DS-大题模板1） |
| [21. 合并两个有序链表](https://leetcode.cn/problems/merge-two-sorted-lists/) | 简单 | 归并思想基础 | 两路归并模板（DS-大题模板3） |
| [141. 环形链表](https://leetcode.cn/problems/linked-list-cycle/) | 简单 | 快慢指针 | 408选择题常考"判断链表是否有环" |
| [160. 相交链表](https://leetcode.cn/problems/intersection-of-two-linked-lists/) | 简单 | 双指针技巧 | 链表操作的综合运用 |
| [83. 删除排序链表中的重复元素](https://leetcode.cn/problems/remove-duplicates-from-sorted-list/) | 简单 | 链表的遍历与删除 | 与408中"删除所有值为x的结点"异曲同工 |
| [876. 链表的中间结点](https://leetcode.cn/problems/middle-of-the-linked-list/) | 简单 | 快慢指针 | 快慢指针是408大题常见技巧 |
| [19. 删除链表的倒数第 N 个结点](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/) | 中等 | 双指针经典 | 408中链表删除的综合运用 |
| [2. 两数相加](https://leetcode.cn/problems/add-two-numbers/) | 中等 | 链表遍历+进位 | 408中链表的实际操作题 |
| [24. 两两交换链表中的节点](https://leetcode.cn/problems/swap-nodes-in-pairs/) | 中等 | 指针操作 | 408中"链表原地重排"的变体 |
| [142. 环形链表 II](https://leetcode.cn/problems/linked-list-cycle-ii/) | 中等 | 快慢指针+数学推导 | 408中链表与数学的结合题 |
| [82. 删除排序链表中的重复元素 II](https://leetcode.cn/problems/remove-duplicates-from-sorted-list-ii/) | 中等 | 双指针/递归 | 408"删除重复元素"的进阶 |
| [143. 重排链表](https://leetcode.cn/problems/reorder-list/) | 中等 | 找中点+反转+合并 | 三步组合题，与408大题思路一致 |

### 刷题策略（针对有编程基础者）

```
第1轮（3天）: 206 → 21 → 83 → 141 → 160 → 876 → 19
             重点：链表基本操作的手速和正确性
第2轮（2天）: 2 → 24 → 82 → 142 → 143
             重点：复杂场景下指针的精细控制
第3轮（1天）: 每道题尝试 递归/非递归 两种写法
             重点：加深对链表本质的理解
```

### 🔥 408与力扣的差异点

| 方面 | 力扣（工程风格） | 408（考试风格） |
|------|-----------------|-----------------|
| 头结点 | 通常无头结点 | **带头结点**是默认约定 |
| 函数签名 | `ListNode* reverseList(ListNode* head)` | `void Reverse(LinkList L)` — L是头指针 |
| 返回值 | 返回新头指针 | 通常void，直接修改链表 |
| 空间要求 | 通常无限制 | 经常要求 **O(1)空间** |
| 下标起始 | 0-based | 408插入删除常用 **1-based 位序** |

> ⚠️ **重要**：做力扣题后，**用408的风格重写一遍**。例如206反转链表，力扣返回新头，而408的`Reverse(LinkList L)`直接修改带头结点的链表。两种写法都要会。

---

## 📖 教材补充：顺序表插入/删除的位置与复杂度细节

### 插入操作

在顺序表第 i（1<=i<=L.length+1）个位置插入新元素 e：
- 移动次数：若在表尾插入（i=n+1），移动 0 次；在表头插入（i=1），移动 n 次
- **平均移动次数** = n/2

### 删除操作

删除第 i（1<=i<=L.length）个位置的元素：
- 移动次数：删除表尾（i=n）移动 0 次；删除表头（i=1）移动 n-1 次
- **平均移动次数** = (n-1)/2

### 关于 realloc

在408代码题中，**通常不要求实现扩容逻辑**。顺序表被简化为一个定长数组 + length 变量。

---

## 📖 教材补充：带头结点 vs 不带头结点的链表

| 场景 | 带头结点 | 不带头结点 |
|------|----------|------------|
| 空表判断 | `L->next == NULL` | `L == NULL` |
| 插入/删除第一个元素 | 与一般位置代码一致 | 需特殊处理头指针 |
| 408大题默认 | ✅ **默认使用** | 只在题目明确时使用 |
| 力扣默认 | ❌ 不带头结点 | ✅ 默认 |

> **408答题建议**：除非题目明确说"不带头结点"，一律用带头结点的写法。

---

## 🔥 408新题补充

### 有序链表去重

```c
void RemoveDuplicates(LinkList L) {
    LNode *p = L->next;
    while (p != NULL && p->next != NULL) {
        if (p->data == p->next->data) {
            LNode *q = p->next;
            p->next = q->next;
            free(q);
        } else {
            p = p->next;
        }
    }
}
// 时间 O(n)，空间 O(1)
```

### 判断链表是否有环（快慢指针）

```c
int HasCycle(LinkList L) {
    LNode *fast = L->next;
    LNode *slow = L->next;
    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return 1;
    }
    return 0;
}
// 时间 O(n)，空间 O(1)
```

---

> 🔗 上一章：[[DS-Ch1-绪论]] | 下一章：[[DS-Ch3-栈和队列]] | [[DS-大题模板]]
