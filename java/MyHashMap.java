import java.util.LinkedList;
import java.util.Objects;

/**
 * A minimal HashMap implementation using separate chaining.
 * - Supports put/get/remove/containsKey
 * - Automatically resizes when load factor exceeds threshold
 */
public class MyHashMap<K, V> {

    private static class Entry<K, V> {
        final K key;
        V value;

        Entry(K key, V value) {
            this.key = key;
            this.value = value;
        }
    }

    private static final int DEFAULT_CAPACITY = 16;
    private static final double DEFAULT_LOAD_FACTOR = 0.75;

    private LinkedList<Entry<K, V>>[] table;
    private int size;
    private final double loadFactor;

    @SuppressWarnings("unchecked")
    public MyHashMap() {
        this.table = (LinkedList<Entry<K, V>>[]) new LinkedList[DEFAULT_CAPACITY];
        this.loadFactor = DEFAULT_LOAD_FACTOR;
        this.size = 0;
    }

    @SuppressWarnings("unchecked")
    public MyHashMap(int initialCapacity, double loadFactor) {
        if (initialCapacity <= 0) {
            throw new IllegalArgumentException("initialCapacity must be > 0");
        }
        if (loadFactor <= 0.0) {
            throw new IllegalArgumentException("loadFactor must be > 0");
        }
        this.table = (LinkedList<Entry<K, V>>[]) new LinkedList[initialCapacity];
        this.loadFactor = loadFactor;
        this.size = 0;
    }

    public int size() {
        return size;
    }

    public int capacity() {
        return table.length;
    }

    public boolean containsKey(K key) {
        return get(key) != null;
    }

    public V get(K key) {
        requireKey(key);
        int idx = indexFor(key, table.length);
        LinkedList<Entry<K, V>> bucket = table[idx];
        if (bucket == null) {
            return null;
        }
        for (Entry<K, V> e : bucket) {
            if (Objects.equals(e.key, key)) {
                return e.value;
            }
        }
        return null;
    }

    public V put(K key, V value) {
        requireKey(key);

        if ((size + 1.0) / table.length > loadFactor) {
            resize(table.length * 2);
        }

        int idx = indexFor(key, table.length);
        if (table[idx] == null) {
            table[idx] = new LinkedList<>();
        }

        for (Entry<K, V> e : table[idx]) {
            if (Objects.equals(e.key, key)) {
                V old = e.value;
                e.value = value;
                return old;
            }
        }

        table[idx].add(new Entry<>(key, value));
        size++;
        return null;
    }

    public V remove(K key) {
        requireKey(key);
        int idx = indexFor(key, table.length);
        LinkedList<Entry<K, V>> bucket = table[idx];
        if (bucket == null) {
            return null;
        }

        for (int i = 0; i < bucket.size(); i++) {
            Entry<K, V> e = bucket.get(i);
            if (Objects.equals(e.key, key)) {
                bucket.remove(i);
                size--;
                return e.value;
            }
        }
        return null;
    }

    public void clear() {
        for (int i = 0; i < table.length; i++) {
            table[i] = null;
        }
        size = 0;
    }

    private void requireKey(K key) {
        if (key == null) {
            throw new IllegalArgumentException("key cannot be null");
        }
    }

    private int indexFor(K key, int mod) {
        int h = key.hashCode();
        // Spread bits a little (simple mixing)
        h ^= (h >>> 16);
        return (h & 0x7fffffff) % mod;
    }

    @SuppressWarnings("unchecked")
    private void resize(int newCapacity) {
        LinkedList<Entry<K, V>>[] old = table;
        table = (LinkedList<Entry<K, V>>[]) new LinkedList[newCapacity];
        size = 0;

        for (LinkedList<Entry<K, V>> bucket : old) {
            if (bucket == null) continue;
            for (Entry<K, V> e : bucket) {
                put(e.key, e.value);
            }
        }
    }
}
