import java.util.NoSuchElementException;

/**
 * A minimal AVL Tree implementation (insert + contains) for demonstration purposes.
 * - Generic type must be Comparable.
 * - Supports insertion (no duplicates) and membership check.
 */
public class AVLTree<T extends Comparable<? super T>> {

    private static class Node<T> {
        T data;
        Node<T> left;
        Node<T> right;
        int height;

        Node(T data) {
            this.data = data;
            this.height = 0;
        }
    }

    private Node<T> root;
    private int size;

    public int size() {
        return size;
    }

    public int height() {
        return height(root);
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public boolean contains(T value) {
        if (value == null) {
            throw new IllegalArgumentException("value cannot be null");
        }
        Node<T> curr = root;
        while (curr != null) {
            int cmp = value.compareTo(curr.data);
            if (cmp == 0) {
                return true;
            } else if (cmp < 0) {
                curr = curr.left;
            } else {
                curr = curr.right;
            }
        }
        return false;
    }

    public void insert(T value) {
        if (value == null) {
            throw new IllegalArgumentException("value cannot be null");
        }
        root = insert(root, value);
    }

    private Node<T> insert(Node<T> node, T value) {
        if (node == null) {
            size++;
            return new Node<>(value);
        }

        int cmp = value.compareTo(node.data);
        if (cmp < 0) {
            node.left = insert(node.left, value);
        } else if (cmp > 0) {
            node.right = insert(node.right, value);
        } else {
            // duplicate: do nothing (or you can update)
            return node;
        }

        updateHeight(node);
        return rebalance(node);
    }

    private Node<T> rebalance(Node<T> node) {
        int bf = balanceFactor(node);

        // Left heavy
        if (bf > 1) {
            // Left-Right case
            if (balanceFactor(node.left) < 0) {
                node.left = rotateLeft(node.left);
            }
            // Left-Left case
            return rotateRight(node);
        }

        // Right heavy
        if (bf < -1) {
            // Right-Left case
            if (balanceFactor(node.right) > 0) {
                node.right = rotateRight(node.right);
            }
            // Right-Right case
            return rotateLeft(node);
        }

        return node;
    }

    private Node<T> rotateLeft(Node<T> a) {
        Node<T> b = a.right;
        Node<T> bLeft = b.left;

        b.left = a;
        a.right = bLeft;

        updateHeight(a);
        updateHeight(b);
        return b;
    }

    private Node<T> rotateRight(Node<T> a) {
        Node<T> b = a.left;
        Node<T> bRight = b.right;

        b.right = a;
        a.left = bRight;

        updateHeight(a);
        updateHeight(b);
        return b;
    }

    private int balanceFactor(Node<T> node) {
        return height(node.left) - height(node.right);
    }

    private void updateHeight(Node<T> node) {
        node.height = Math.max(height(node.left), height(node.right)) + 1;
    }

    private int height(Node<T> node) {
        return node == null ? -1 : node.height;
    }

    // Optional helper: get min (useful for validating structure)
    public T min() {
        if (root == null) {
            throw new NoSuchElementException("tree is empty");
        }
        Node<T> curr = root;
        while (curr.left != null) {
            curr = curr.left;
        }
        return curr.data;
    }
}
