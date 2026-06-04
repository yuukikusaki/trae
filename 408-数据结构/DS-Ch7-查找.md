---
tags: [408, 数据结构, Ch7, 查找, 二分查找, B树, 哈希表]
aliases: [DS第七章, 查找]
---

# DS-Ch7-查找

[[DS-MOC-数据结构总览|MOC]] | 上一章：[[DS-Ch6-图]] | 下一章：[[DS-Ch8-排序]] | [[DS-大题模板]]

---

## 7.1 查找的基本概念

**查找表**：由同一类型的数据元素构成的集合。
**关键字**：数据元素中唯一标识该元素的某个数据项的值。
**平均查找长度 ASL**：查找算法中关键字的平均比较次数。

$$
ASL = \sum_{i=1}^{n} P_i \cdot C_i
$$

- $P_i$：查找第 $i$ 个元素的概率
- $C_i$：查找到第 $i$ 个元素所需的比较次数

---

## 7.2 顺序查找

### 7.2.1 基本思想

从头到尾依次比较，找到返回位置，找不到返回 -1。

### 7.2.2 无哨兵版本

```c
#include <stdio.h>

//==408考点== 顺序查找（无哨兵），每轮循环需要检查两个条件
int SeqSearch(int arr[], int n, int key) {
    for (int i = 0; i < n; i++) {   // 条件1：i < n
        if (arr[i] == key)          // 条件2：arr[i] == key
            return i;
    }
    return -1;
}
```

### 7.2.3 哨兵技巧（408 常考优化）

**核心思想**：将待查找的 key 放在 a[0]（或 a[n]），省去边界检查。**每轮循环只需判断一个条件**。

```c
//==408考点== 哨兵法：a[0] 留空作为哨兵，数据从 a[1] 开始存放
int SeqSearch_Sentinel(int arr[], int n, int key) {
    arr[0] = key;                    // 设置哨兵
    int i;
    for (i = n; arr[i] != key; i--); // 只判断一个条件！
    return i;                        // i==0 表示未找到
}

// 测试
int main() {
    int a[11] = {0, 23, 45, 12, 67, 89, 34, 56, 78, 90, 10}; // a[0] 留给哨兵
    int key = 67;
    int pos = SeqSearch_Sentinel(a, 10, key);
    printf("哨兵查找 %d: %s, 位置=%d\n", key, pos ? "找到" : "未找到", pos);
    return 0;
}
```

**ASL 分析**：
- 等概率查找成功：$ASL_{成功} = \frac{n+1}{2}$
- 查找失败：$ASL_{失败} = n+1$（无哨兵）/ $n+1$（有哨兵，始终比较到哨兵）
- 时间复杂度：$O(n)$

> **408 技巧**：哨兵的本质是"用空间换时间减少条件判断"。选择题常考"哨兵存放在哪个位置"。

---

## 7.3 二分查找（折半查找）

**前提**：有序顺序表（**必须支持随机存取**，链表不行）。

### 7.3.1 非递归实现

```c
#include <stdio.h>

//==408考点== 二分查找非递归，注意 mid 公式的防溢出写法
int BinarySearch(int arr[], int n, int key) {
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        //==408考点== lo+(hi-lo)/2 防溢出，(lo+hi)/2 可能溢出
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] == key)
            return mid;
        else if (arr[mid] > key)
            hi = mid - 1;
        else
            lo = mid + 1;
    }
    return -1;
}
```

### 7.3.2 递归实现

```c
//==408考点== 二分查找递归实现
int BinarySearch_Recursive(int arr[], int lo, int hi, int key) {
    if (lo > hi) return -1;                     // 递归出口
    int mid = lo + (hi - lo) / 2;
    if (arr[mid] == key) return mid;
    else if (arr[mid] > key)
        return BinarySearch_Recursive(arr, lo, mid - 1, key);
    else
        return BinarySearch_Recursive(arr, mid + 1, hi, key);
}
```

### 7.3.3 判定树与 ASL

二分查找过程可用**二叉判定树**描述，树高 $\lceil \log_2(n+1) \rceil$。

**ASL 公式**（等概率）：
- $ASL_{成功} = \frac{1}{n} \sum_{i=1}^{n} l_i$，其中 $l_i$ 为第 $i$ 个结点所在层数
- $ASL_{失败} \approx \log_2(n+1)$

> **408 考点**：对于 n 个结点的判定树，成功 ASL 可用 $\frac{n+1}{n}\log_2(n+1)-1$ 近似。

时间复杂度：$O(\log n)$，空间复杂度：非递归 $O(1)$，递归 $O(\log n)$。

### 7.3.4 mid 公式讨论

| 公式 | 优劣 |
|------|------|
| `(lo + hi) / 2` | lo+hi 可能 int 溢出 |
| `lo + (hi - lo) / 2` | **防溢出，推荐** |
| `lo + ((hi - lo) >> 1)` | 位运算加速，同样防溢出 |

```c
//==408考点== 三种 mid 公式
int mid1 = (lo + hi) / 2;       // 可能溢出，不推荐
int mid2 = lo + (hi - lo) / 2;  // 安全，408标准写法
int mid3 = lo + ((hi-lo) >> 1); // 位运算优化版本
```

---

## 7.4 分块查找（索引顺序查找）

**思想**：将数据分成若干块，块间有序、块内无序。建立索引表存储每块的最大关键字和起始地址。

```c
#include <stdio.h>

// 索引表结构
typedef struct {
    int maxKey;     // 块内最大关键字
    int start;      // 块的起始下标
    int length;     // 块长度
} Index;

//==408考点== 分块查找
int BlockSearch(int arr[], int n, Index idx[], int m, int key) {
    // 第一步：二分查找确定所在块
    int blockIdx = -1;
    int lo = 0, hi = m - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (idx[mid].maxKey >= key) {
            blockIdx = mid;
            hi = mid - 1;  // 找第一个 maxKey >= key 的块
        } else {
            lo = mid + 1;
        }
    }
    if (blockIdx == -1) return -1;

    // 第二步：块内顺序查找
    for (int i = idx[blockIdx].start;
         i < idx[blockIdx].start + idx[blockIdx].length; i++) {
        if (arr[i] == key) return i;
    }
    return -1;
}

int main() {
    int arr[] = {8, 3, 5,    // 第0块，max=8
                 12, 9, 15,   // 第1块，max=15
                 22, 18, 25}; // 第2块，max=25
    Index idx[3] = {
        {8,  0, 3},
        {15, 3, 3},
        {25, 6, 3}
    };
    int pos = BlockSearch(arr, 9, idx, 3, 12);
    printf("分块查找 12: %s, 位置=%d\n", pos >= 0 ? "找到" : "未找到", pos);
    return 0;
}
```

**时间复杂度**：$O(\sqrt{n})$（当块数 = 块长 = $\sqrt{n}$ 时最优）。

---

## 7.5 二叉排序树 BST 查找（回顾 Ch5）

> 详细内容见 [[DS-Ch5-树与二叉树]]。本章仅从查找角度简要回顾。

```c
// BST 结点
typedef struct BSTNode {
    int key;
    struct BSTNode *left, *right;
} BSTNode;

//==408考点== BST 查找（递归）
BSTNode* BST_Search(BSTNode *root, int key) {
    if (root == NULL) return NULL;
    if (key == root->key) return root;
    else if (key < root->key)
        return BST_Search(root->left, key);
    else
        return BST_Search(root->right, key);
}

//==408考点== BST 查找（非递归）
BSTNode* BST_Search_Iter(BSTNode *root, int key) {
    while (root != NULL && key != root->key) {
        if (key < root->key)
            root = root->left;
        else
            root = root->right;
    }
    return root;
}
```

**分析**：
- 最好：$O(\log n)$（平衡时）
- 最坏：$O(n)$（退化成单链表）
- **BST 查找性能取决于树的高度**

---

## 7.6 平衡二叉树 AVL 回顾

**定义回顾**：左右子树高度差不超过 1 的 BST。查找操作与 BST 完全相同，$O(\log n)$ 稳定。

> AVL 的插入旋转（LL/RR/LR/RL）详见 [[DS-Ch5-树与二叉树]]。

---

## 7.7 B 树（408 大题重点）

### 7.7.1 m 阶 B 树定义

**m 阶 B 树**是满足以下性质的 m 叉查找树：

| 条件 | 根结点 | 非根内部结点 |
|------|--------|--------------|
| 最少子树 | 2（非叶时） | $\lceil m/2 \rceil$ |
| 最少关键字 | 1（非叶时） | $\lceil m/2 \rceil - 1$ |
| 最多子树 | m | m |
| 最多关键字 | m-1 | m-1 |

**关键性质**：
1. 所有叶结点在同一层（平衡）
2. 结点中关键字有序：$K_1 < K_2 < \dots < K_n$
3. 子树与关键字交错：指针 $P_i$ 指向的子树中所有关键字在 $(K_{i-1}, K_i)$ 之间

```
B树结点结构（以关键字 20, 40, 60 为例）：
┌──────┬──────┬──────┐
│  20  │  40  │  60  │   ← 关键字，最多 m-1 个
└──────┴──────┴──────┘
  /    /      /      \
 P0   P1     P2       P3   ← 子树指针，最多 m 个
(<20) (20,40) (40,60) (>60)
```

### 7.7.2 B 树结点定义（C 代码）

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define M 5           // B树阶数，以5阶为例（408常考3阶/5阶）
#define MAX_KEY (M-1)  // 最多关键字数 = 4
#define MIN_KEY ((M+1)/2 - 1)  // 最少关键字数 = 2

typedef struct BTreeNode {
    int keys[M];                // 关键字数组，下标从1开始，0号位保留
    struct BTreeNode *children[M + 1]; // 子树指针数组
    int keyNum;                 // 当前关键字数量
    bool isLeaf;                // 是否为叶结点
} BTreeNode;
```

### 7.7.3 B 树查找

```c
//==408考点== B树查找
BTreeNode* BTree_Search(BTreeNode *root, int key) {
    if (root == NULL) return NULL;

    int i = 1;
    // 在当前结点中找到第一个 >= key 的位置
    while (i <= root->keyNum && key > root->keys[i])
        i++;

    if (i <= root->keyNum && root->keys[i] == key)
        return root;  // 找到

    if (root->isLeaf)
        return NULL;  // 到叶结点还没找到，查找失败

    // 递归查找子树
    return BTree_Search(root->children[i - 1], key);
}
```

### 7.7.4 B 树插入与分裂（408 大题最爱）

**插入流程**：先定位到叶子结点插入；若关键字超限（>=m），则**分裂**。

**分裂操作（以 5 阶 B 树为例）**：

```
插入导致结点关键字变为 5 个（超过 m-1=4），需要分裂：

分裂前（1个结点）：
[10, 20, 30, 40, 50]  keyNum=5 >= M，触发分裂

↑ 中间关键字 30 上升到父结点

分裂后（1父 + 2子）：
         [30]
        /    \
  [10, 20]   [40, 50]
```

**核心代码**：

```c
//==408考点== 分裂子结点
void BTree_SplitChild(BTreeNode *parent, int idx) {
    // idx: 要分裂的子结点在 parent->children 中的位置
    BTreeNode *child = parent->children[idx];
    BTreeNode *newNode = (BTreeNode*)calloc(1, sizeof(BTreeNode));
    newNode->isLeaf = child->isLeaf;

    int mid = (M + 1) / 2;  // 中间关键字位置（上取整）

    // 1. 将 child 的后半部分关键字移到 newNode
    newNode->keyNum = child->keyNum - mid;
    for (int j = 1; j <= newNode->keyNum; j++)
        newNode->keys[j] = child->keys[mid + j];

    // 2. 若不是叶子，也要移动后半部分的子树指针
    if (!child->isLeaf) {
        for (int j = 1; j <= newNode->keyNum + 1; j++)
            newNode->children[j] = child->children[mid + j];
    }

    // 3. 更新 child 的关键字数量
    child->keyNum = mid - 1;

    // 4. 将 parent 中的指针后移，腾出位置
    for (int j = parent->keyNum; j >= idx + 1; j--)
        parent->children[j + 1] = parent->children[j];
    parent->children[idx + 1] = newNode;

    // 5. 将中间关键字提升到 parent
    for (int j = parent->keyNum; j >= idx; j--)
        parent->keys[j + 1] = parent->keys[j];
    parent->keys[idx + 1] = child->keys[mid];
    parent->keyNum++;
}

//==408考点== B树插入（包装）
void BTree_InsertNonFull(BTreeNode *node, int key) {
    int i = node->keyNum;
    if (node->isLeaf) {
        // 叶子结点：找到插入位置，直接插入
        while (i >= 1 && key < node->keys[i]) {
            node->keys[i + 1] = node->keys[i];
            i--;
        }
        node->keys[i + 1] = key;
        node->keyNum++;
    } else {
        // 非叶结点：找到要下的子树
        while (i >= 1 && key < node->keys[i])
            i--;
        i++;  // 子树下标

        // 如果子树已满，先分裂
        if (node->children[i]->keyNum == MAX_KEY) {
            BTree_SplitChild(node, i);
            if (key > node->keys[i]) i++;
        }
        BTree_InsertNonFull(node->children[i], key);
    }
}
```

### 7.7.5 B 树删除与合并（手算演示）

**删除流程**分三种情况：

**情况1**：删除的关键字在**叶结点**且删除后依然满足最小关键字数。
```
例：5阶B树，叶结点 [10, 20, 30]，删除 20
删除后：[10, 30]，keyNum=2 >= 2，OK
```

**情况2**：删除的关键字在**非叶结点**。
- 找到前驱（左子树最大关键字）或后继（右子树最小关键字）替换
- 转化为在叶结点删除前驱/后继

```
例：删除 50（非叶结点）
        [50]
       /    \
  [10,20]  [60,70]

用后继 60 替换，然后在右子树叶结点删除 60：
        [60]
       /    \
  [10,20]  [70]
```

**情况3**：删除后叶结点关键字数不足，需要**借**或**合并**。

```
借兄弟：
删除前：parent [30, 60]，左子 [10]，右子 [40, 50]
         [30,  60]
        /    |    \
     [10]  [40,50]  [...]

删除左子的某个关键字导致不足，找右兄弟借：
右兄弟有富余（keyNum > MIN_KEY），借一个：
父关键字 30 下移到左子，右兄弟最小关键字 40 上移到父：
         [40,  60]
        /    |    \
     [10,30] [50]  [...]
```

**合并**（兄弟也穷，keyNum == MIN_KEY）：
```
合并前：parent [60]，左子 [10, 30]，右子 [80]
         [60]
        /    \
    [10,30] [80]

左子满（含 MIN_KEY=2 个关键字），右子穷（只有1个，刚好MIN_KEY）。
将父关键字 60 拉下来与右兄弟合并：
         (空)
          |
    [10, 30, 60, 80]

父结点可能因此变空，继续向上递归处理。
```

> **408 大题手算要点**：删除操作先判断能不能直接删，不能就分"借兄弟"或"合并"两步走。**方向优先看左兄弟，左兄弟不够再看右兄弟**。

---

## 7.8 B+ 树

### 7.8.1 定义

m 阶 B+ 树与 B 树的核心区别：

| 特性 | B 树 | B+ 树 |
|------|------|-------|
| 关键字分布 | 每个结点都存关键字+记录 | 非叶结点只存**索引**（仅关键字），记录全在叶子 |
| 叶子结点 | 孤立 | 按关键字**顺序链接成链表** |
| 查找路径 | 可能在内部结点命中 | **必须查到叶子**才知是否存在 |
| 分支因子 | 内部结点最多 m-1 个关键字 | 内部结点最多 m 个关键字（有的教材为 m-1） |
| 应用 | 文件系统（极少用） | 数据库索引（MySQL InnoDB） |

```
B+树结构示意：
               [30, 60]          ← 非叶结点：仅索引
              /    |    \
     [10,20] -> [30,40,50] -> [60,70,80]  ← 叶结点：存数据
     ↑                        ↑
     └── 双向链表连接 ────────┘
```

### 7.8.2 B+ 树查找（关键代码）

```c
//==408考点== B+树查找：必须搜索到叶结点
BTreeNode* BPlusTree_Search(BTreeNode *root, int key) {
    BTreeNode *cur = root;
    // 一直下到叶结点
    while (!cur->isLeaf) {
        int i = 1;
        while (i <= cur->keyNum && key >= cur->keys[i])
            i++;
        cur = cur->children[i - 1];
    }
    // 在叶结点中查找
    for (int i = 1; i <= cur->keyNum; i++) {
        if (cur->keys[i] == key)
            return cur;
    }
    return NULL;
}
```

### 7.8.3 B 树 vs B+ 树（408 选择题高频对比）

| 对比维度 | B 树 | B+ 树 |
|----------|------|-------|
| 查找终止 | 任意层都可能终止 | **必须到叶子** |
| 非叶结点 | 存关键字+记录 | 仅存索引（关键字） |
| 叶结点链表 | 无 | 有，支持**范围查找** |
| 相同关键字数存更多数据 | 否 | 是（非叶不存记录） |

> **408 记法**：B+ 树"+"在叶子链表支持范围查询。数据库用 B+ 树而非 B 树，因为范围查询是高频操作。

---

## 7.9 哈希表

### 7.9.1 基本概念

**哈希函数** $H(key)$：把关键字映射到地址空间。
**冲突**：$H(key_1) = H(key_2)$ 但 $key_1 \neq key_2$。
**装填因子** $\alpha = \frac{表中记录数}{表长}$，反映表的装满程度。

### 7.9.2 常见哈希函数

```c
//==408考点== 除留余数法：H(key) = key % p
// p 取不大于表长的最大素数，能减少冲突
int Hash_Division(int key, int p) {
    return key % p;
}

// 408 常考：表长 m=13，取 p=13
// p 选择原则：p 不大于 m 的最大素数
```

### 7.9.3 开放定址法（处理冲突）

**核心公式**：
$$H_i = (H(key) + d_i) \% m$$

根据 $d_i$ 的取法不同分为：

#### (1) 线性探测法

$d_i = 0, 1, 2, \dots, m-1$

```c
#include <stdio.h>
#include <stdbool.h>

#define TABLE_SIZE 13
#define EMPTY -1

typedef struct {
    int key;
    bool occupied;   // 是否被占用
    bool deleted;    // 是否被删除（408考点：删除需打标记而非置空）
} HashTable;

HashTable ht[TABLE_SIZE];

// 初始化
void InitHashTable() {
    for (int i = 0; i < TABLE_SIZE; i++) {
        ht[i].key = 0;
        ht[i].occupied = false;
        ht[i].deleted = false;
    }
}

//==408考点== 哈希表插入（线性探测法）
bool HashInsert_Linear(int key) {
    int hash = key % TABLE_SIZE;
    int d = 0;
    // 线性探测：d_i = 0, 1, 2, ...
    while (d < TABLE_SIZE) {
        int addr = (hash + d) % TABLE_SIZE;
        if (!ht[addr].occupied || ht[addr].deleted) {
            ht[addr].key = key;
            ht[addr].occupied = true;
            ht[addr].deleted = false;
            return true;
        }
        d++;
    }
    return false; // 表满
}

//==408考点== 哈希表查找（线性探测法）
int HashSearch_Linear(int key) {
    int hash = key % TABLE_SIZE;
    int d = 0;
    while (d < TABLE_SIZE) {
        int addr = (hash + d) % TABLE_SIZE;
        if (!ht[addr].occupied)
            return -1;  // 遇到空位，查找失败
        if (ht[addr].key == key && !ht[addr].deleted)
            return addr; // 找到
        d++;
    }
    return -1; // 找了一圈没找到
}

//==408考点== 删除必须打标记，不能直接置空
bool HashDelete_Linear(int key) {
    int addr = HashSearch_Linear(key);
    if (addr == -1) return false;
    ht[addr].deleted = true;  // 打删除标记
    // ht[addr].occupied 保持不变！
    return true;
}
```

**聚集问题**：线性探测容易产生**一次聚集**——同义词和非同义词互相冲突堆积。

#### (2) 平方探测法（二次探测）

$d_i = 1^2, -1^2, 2^2, -2^2, \dots$

```c
//==408考点== 平方探测法
bool HashInsert_Quadratic(int key) {
    int hash = key % TABLE_SIZE;
    int sign = 1;
    for (int k = 1; k <= TABLE_SIZE / 2; k++) {
        int d = sign * k * k;  // +1, -1, +4, -4, +9, -9, ...
        int addr = ((hash + d) % TABLE_SIZE + TABLE_SIZE) % TABLE_SIZE;
        if (!ht[addr].occupied || ht[addr].deleted) {
            ht[addr].key = key;
            ht[addr].occupied = true;
            ht[addr].deleted = false;
            return true;
        }
        sign = -sign;  // 交替正负
    }
    return false;
}
```

**条件**：表长 m 必须是 $4k+3$ 形式的素数才能探测到整个表。

#### (3) 双散列法

$d_i = i \times H_2(key)$，两个哈希函数配合。

```c
//==408考点== 双散列法
int Hash2(int key) {
    return 7 - (key % 7);  // 第二个哈希函数
}

bool HashInsert_Double(int key) {
    int hash = key % TABLE_SIZE;
    int step = Hash2(key);
    for (int i = 0; i < TABLE_SIZE; i++) {
        int addr = (hash + i * step) % TABLE_SIZE;
        if (!ht[addr].occupied || ht[addr].deleted) {
            ht[addr].key = key;
            ht[addr].occupied = true;
            ht[addr].deleted = false;
            return true;
        }
    }
    return false;
}
```

### 7.9.4 链地址法（拉链法）

将所有同义词用链表链接在同一个槽位上。

```c
#include <stdlib.h>

//==408考点== 链地址法
typedef struct HashNode {
    int key;
    struct HashNode *next;
} HashNode;

HashNode *chain[TABLE_SIZE];  // 指针数组，每个槽一个链表

void Chain_Init() {
    for (int i = 0; i < TABLE_SIZE; i++)
        chain[i] = NULL;
}

void Chain_Insert(int key) {
    int addr = key % TABLE_SIZE;
    HashNode *node = (HashNode*)malloc(sizeof(HashNode));
    node->key = key;
    node->next = chain[addr];   //==408考点== 头插法，O(1)
    chain[addr] = node;
}

HashNode* Chain_Search(int key) {
    int addr = key % TABLE_SIZE;
    HashNode *cur = chain[addr];
    while (cur != NULL) {
        if (cur->key == key)
            return cur;
        cur = cur->next;
    }
    return NULL;
}

bool Chain_Delete(int key) {
    int addr = key % TABLE_SIZE;
    HashNode *cur = chain[addr], *prev = NULL;
    while (cur != NULL) {
        if (cur->key == key) {
            if (prev) prev->next = cur->next;
            else chain[addr] = cur->next;
            free(cur);
            return true;
        }
        prev = cur;
        cur = cur->next;
    }
    return false;
}
```

### 7.9.5 处理冲突方法对比

| 方法 | 优点 | 缺点 |
|------|------|------|
| 线性探测 | 实现简单 | **一次聚集**，性能严重下降 |
| 平方探测 | 减轻一次聚集 | **二次聚集**，表长必须是 4k+3 素数 |
| 双散列 | 无聚集问题 | 计算量稍大 |
| 链地址法 | 无聚集，删除方便 | 额外指针空间，链表遍历开销 |

---

## 7.10 哈希表 ASL 计算（408 选择题高频）

### 7.10.1 手工计算 ASL

**写在前面**：ASL 手算是 408 选择必考题，必须掌握线性探测的手动推演过程。

**示例**：表长 m=13，哈希函数 H(key)=key%13，用线性探测法处理冲突。
依次插入：19, 14, 23, 01, 68, 20, 84, 27, 55, 11, 10, 79

**手推过程**：

```
key=19: H=19%13=6  →  6:19
key=14: H=14%13=1  →  1:14
key=23: H=23%13=10 → 10:23
key=01: H=1%13=1   →  冲突→2:01
key=68: H=68%13=3  →  3:68
key=20: H=20%13=7  →  7:20
key=84: H=84%13=6  →  冲突→7→8:84
key=27: H=27%13=1  →  冲突→2→3→4:27
key=55: H=55%13=3  →  冲突→4→5:55
key=11: H=11%13=11 → 11:11
key=10: H=10%13=10 → 冲突→11→12:10
key=79: H=79%13=1  → 冲突→2→3→4→5→6→7→8→9:79
```

最终哈希表：

| 地址 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|------|---|---|---|---|---|---|---|---|---|---|---|----|----|----|
| 关键字 | - | 14 | 01 | 68 | 27 | 55 | 19 | 20 | 84 | 79 | 23 | 11 | 10 |
| 探测次数 | - | 1 | 2 | 1 | 4 | 3 | 1 | 1 | 3 | 9 | 1 | 1 | 3 |

**ASL 计算**：

$$ASL_{成功} = \frac{1+2+1+4+3+1+1+3+9+1+1+3}{12} = \frac{30}{12} = 2.5$$

**查找失败的 ASL**（线性探测法）：对每个地址，计算从该地址开始直到遇到空位为止的比较次数。

```
地址0: H=0，0空→比较0次? 根据408惯例为1次（与空位比较也算）
实际408标准：地址0为空，比较1次即确定失败（因为空位意味着不存在）

地址1: 1:14→2:01→3:68→4:27→5:55→6:19→7:20→8:84→9:79→10:23→11:11→12:10→0空
→比较了13次

以此类推每个地址...最终求平均值。

注：不同教材对"空地址比较次数"的算法有差异，
408通常以"遇到空位说明查找失败，比较次数+1"计算。
```

### 7.10.2 链地址法 ASL 计算

**查找成功**：
$$ASL_{成功} = \frac{1}{n} \sum_{i=1}^{m} \frac{L_i(L_i+1)}{2}$$

其中 $L_i$ 为第 i 条链的长度，n 为总关键字数。

**查找失败**：
$$ASL_{失败} = \frac{n}{m} = \alpha$$

（链地址法查找失败时，平均比较次数等于平均链长）

---

## 7.11 装填因子 $\alpha$ 对性能的影响

$$\alpha = \frac{n}{m}$$

| $\alpha$ | 含义 |
|-----------|------|
| 越小 | 表越空，冲突越少，查找越快，空间浪费大 |
| 越大 | 表越满，冲突越多，查找越慢 |
| 经验值 | 开放定址法 $\alpha < 0.5$，链地址法 $\alpha$ 可以接近 1 |

**链地址法下哈希表的平均查找长度**：
$$ASL_{成功} \approx 1 + \frac{\alpha}{2}$$
$$ASL_{失败} \approx \alpha + e^{-\alpha}$$

```c
//==408考点== 装填因子计算示例
double Alpha(int records, int tableSize) {
    return (double)records / tableSize;
}
// 例：表长13，装了8条记录，α = 8/13 ≈ 0.615
```

---

## 7.12 各种查找算法复杂度对比表

| 查找算法 | 平均时间 | 最坏时间 | 空间 | 适用条件 |
|----------|----------|----------|------|----------|
| 顺序查找 | $O(n)$ | $O(n)$ | $O(1)$ | 无序、链表均可 |
| 二分查找 | $O(\log n)$ | $O(\log n)$ | $O(1)$ | 有序顺序表 |
| 分块查找 | $O(\sqrt{n})$ | $O(n)$ | $O(1)$ | 分块有序 |
| BST 查找 | $O(\log n)$ | $O(n)$ | $O(1)$ | — |
| AVL 查找 | $O(\log n)$ | $O(\log n)$ | $O(1)$ | — |
| B 树查找 | $O(\log n)$ | $O(\log n)$ | $O(1)$ | 外存数据 |
| B+ 树查找 | $O(\log n)$ | $O(\log n)$ | $O(1)$ | 数据库索引 |
| 哈希表查找 | $O(1)$ | $O(n)$ | $O(n)$ | — |

> **408 记法**：只有顺序查找不要求有序；只有哈希表期望 $O(1)$；BST 可能退化到 $O(n)$。

---

## 7.13 408 易错点

### 易错点 1：二分查找的前提
> **必须是能随机存取的顺序表，链表不能用二分查找！**

### 易错点 2：mid 公式溢出
> `(lo+hi)/2` 在 lo 和 hi 很大时可能 int 溢出，408 推荐 `lo+(hi-lo)/2`。

### 易错点 3：二分查找判定树
> n 个结点的判定树中，失败结点是 n+1 个（成功结点之间的间隙）。
> 判定树高度 $\lceil \log_2(n+1) \rceil$ 是失败 ASL 的上界。

### 易错点 4：B 树根结点特例
> 根结点没有最少关键字限制（可以只有 1 个关键字）。插入导致根结点分裂时，树高 +1。

### 易错点 5：B+ 树内部结点
> B+ 树内部结点不存数据，查找必须到叶结点。**这一点选择题反复考**。

### 易错点 6：哈希表删除
> 开放定址法下删除必须打标记（tombstone），不能直接置空！否则会导致查找路径中断。

### 易错点 7：线性探测 ASL 手算
> 查找失败 ASL 计算时，对每个地址都要算"直到遇到空位"的比较次数。空地址本身也算 1 次比较（不同教材有差异，408 以官方答案为准）。

### 易错点 8：装填因子
> 装填因子增大 → 冲突增多 → ASL 增大。**ASL 只依赖于装填因子**，不直接依赖于 n 或 m 单独的值。

### 易错点 9：分块查找的块内查找
> 块内无序，所以**块内只能顺序查找**。索引表有序，所以**索引表可以二分查找**。

### 易错点 10：B 树删除的借与并
> 借兄弟时，被借的关键字**通过父结点中转**，不是直接移过去。这是手算时最容易画错的地方。

---

[[DS-MOC-数据结构总览|MOC]] | 上一章：[[DS-Ch6-图]] | 下一章：[[DS-Ch8-排序]] | [[DS-大题模板]]
