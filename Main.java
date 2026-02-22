public class Main {
    public static void main(String[] args) {
        // AVL demo
        AVLTree<Integer> avl = new AVLTree<>();
        int[] values = {10, 20, 30, 40, 50, 25};
        for (int v : values) avl.insert(v);

        System.out.println("AVL size = " + avl.size());
        System.out.println("AVL height = " + avl.height());
        System.out.println("AVL contains 25? " + avl.contains(25));
        System.out.println("AVL min = " + avl.min());

        // HashMap demo
        MyHashMap<String, Integer> map = new MyHashMap<>();
        map.put("apple", 3);
        map.put("banana", 5);
        map.put("banana", 6);

        System.out.println("Map size = " + map.size());
        System.out.println("banana = " + map.get("banana"));
        System.out.println("remove apple => " + map.remove("apple"));
        System.out.println("Map size = " + map.size());
        System.out.println("Map capacity = " + map.capacity());
    }
}