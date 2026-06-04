---
tags: [408, 数据结构, 大题, 模板]
aliases: [大题模板, 408手写代码]
---

# 408 数据结构大题模板

> 🔗 [[DS-MOC-数据结构总览|MOC]] | [[DS-复杂度速查]] | 各章笔记：[[DS-Ch2-线性表]] · [[DS-Ch5-树与二叉树]] · [[DS-Ch8-排序]]

---

## 模板 1：链表原地逆置 ⭐⭐⭐

> 408 出现概率最高的代码题之一，必须能手写。

```c
// 三指针法：pre, cur, next
void Reverse(LinkList L) {
    LNode *pre = NULL, *cur = L->next, *next;
    while (cur != NULL) {
        next = cur->next;   // ①暂存后继
        cur->next = pre;    // ②反转指向
        pre = cur;          // ③pre 前进
        cur = next;         // ④cur 前进
    }
    L->next = pre;          // 头结点指向新的首结点
}
// 时间 O(n)，空间 O(1)
```

---

## 模板 2：删除链表中所有值为 x 的结点

```c
// 带头结点
void DeleteX(LinkList L, int x) {
    LNode *p = L, *q;
    while (p->next != NULL) {
        if (p->next->data == x) {
            q = p->next;
            p->next = q->next;
            free(q);
        } else {
            p = p->next;
        }
    }
}
// 时间 O(n)，空间 O(1)
```

---

## 模板 3：两个有序链表的归并

```c
// 归并为递增有序链表（尾插法）
LinkList Merge(LinkList A, LinkList B) {
    LinkList C = (LinkList)malloc(sizeof(LNode));
    C->next = NULL;
    LNode *pa = A->next, *pb = B->next, *pc = C;
    while (pa && pb) {
        if (pa->data <= pb->data) {
            pc->next = pa; pa = pa->next;
        } else {
            pc->next = pb; pb = pb->next;
        }
        pc = pc->next;
    }
    pc->next = pa ? pa : pb;  // 接上剩余部分
    return C;
}
// 时间 O(m+n)，空间 O(1)
```

---

## 模板 4：二叉树递归遍历 ⭐⭐⭐

```c
void PreOrder(BiTree T) {
    if (T) {
        visit(T);               // 访问根
        PreOrder(T->lchild);    // 遍历左子树
        PreOrder(T->rchild);    // 遍历右子树
    }
}

void InOrder(BiTree T) {
    if (T) {
        InOrder(T->lchild);
        visit(T);
        InOrder(T->rchild);
    }
}

void PostOrder(BiTree T) {
    if (T) {
        PostOrder(T->lchild);
        PostOrder(T->rchild);
        visit(T);
    }
}
// 三种遍历均为 O(n)，O(h) 栈空间
```

---

## 模板 5：二叉树非递归中序遍历 ⭐⭐

```c
void InOrder2(BiTree T) {
    SqStack S; InitStack(&S);
    BiTree p = T;
    while (p || !StackEmpty(&S)) {
        if (p) {                 // 一路向左入栈
            Push(&S, p);
            p = p->lchild;
        } else {                 // 左子树空，弹出访问，转向右子树
            Pop(&S, &p);
            visit(p);
            p = p->rchild;
        }
    }
}
// O(n), O(h)
```

---

## 模板 6：二叉树层序遍历 ⭐

```c
void LevelOrder(BiTree T) {
    SqQueue Q; InitQueue(&Q);
    EnQueue(&Q, T);
    while (!QueueEmpty(&Q)) {
        BiTree p; DeQueue(&Q, &p);
        visit(p);
        if (p->lchild) EnQueue(&Q, p->lchild);
        if (p->rchild) EnQueue(&Q, p->rchild);
    }
}
// O(n), O(w) — w 为最大宽度
```

---

## 模板 7：顺序表删除所有 x（双指针）⭐

```c
// k 指向"下一个有效位置"，i 扫描原数组
int DeleteX(SeqList *L, int x) {
    int k = 0;
    for (int i = 0; i < L->length; i++)
        if (L->elem[i] != x)
            L->elem[k++] = L->elem[i];
    L->length = k;
    return 1;
}
// O(n), O(1)
```

---

## 模板 8：二分查找 ⭐⭐

```c
int BinarySearch(int a[], int n, int key) {
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;  // 防溢出
        if (a[mid] == key) return mid;
        else if (a[mid] < key) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
// O(log n)
```

---

## 模板 9：KMP 的 next 数组手算 ⭐⭐

```
步骤：
① 写出模式串 P（下标从 1 开始）
② next[1] = 0, next[2] = 1
③ 对于 j≥3：找 P[1..j-1] 的最长相等前后缀长度 + 1

示例：P = "abaabc"
j=1: next=0
j=2: next=1
j=3: P[1..2]="ab" → 无相等前后缀 → next=1
j=4: P[1..3]="aba" → "a" = "a" → 长度1 → next=2
j=5: P[1..4]="abaa" → "a" = "a" → 长度1 → next=2
j=6: P[1..5]="abaab" → "ab" = "ab" → 长度2 → next=3
next = [0,1,1,2,2,3]
```

---

## 🔥 408 大题应试策略

| 策略 | 说明 |
|------|------|
| **先写注释思路** | 先写 `// 思路：双指针...` 再写代码，思路对拿过程分 |
| **注意边界** | 链表判 `NULL`、循环队列判满判空、数组下标不越界 |
| **复杂度必标** | 每个函数末尾写 `// O(n), O(1)` |
| **先保正确再优化** | O(n²) 暴力的过程分 > O(n) 优化但写错的 0 分 |
| **时间分配** | 代码题 15 分钟：5 分钟思路 + 8 分钟写代码 + 2 分钟检查 |

---

> 🔗 返回 [[DS-MOC-数据结构总览|MOC]] | [[DS-复杂度速查]]
