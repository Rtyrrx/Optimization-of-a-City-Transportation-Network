import java.util.*;

public class KruskalAlgorithm {
    private long operationsCount;

    // Union-Find (Disjoint Set Union) data structure
    private static class UnionFind {
        private final Map<String, String> parent;
        private final Map<String, Integer> rank;

        public UnionFind(Set<String> vertices) {
            parent = new HashMap<>();
            rank = new HashMap<>();
            for (String vertex : vertices) {
                parent.put(vertex, vertex);
                rank.put(vertex, 0);
            }
        }

        public String find(String vertex) {
            if (!parent.get(vertex).equals(vertex)) {
                parent.put(vertex, find(parent.get(vertex))); // Path compression
            }
            return parent.get(vertex);
        }

        public boolean union(String vertex1, String vertex2) {
            String root1 = find(vertex1);
            String root2 = find(vertex2);

            if (root1.equals(root2)) {
                return false; // Already in same set
            }

            // Union by rank
            int rank1 = rank.get(root1);
            int rank2 = rank.get(root2);

            if (rank1 < rank2) {
                parent.put(root1, root2);
            } else if (rank1 > rank2) {
                parent.put(root2, root1);
            } else {
                parent.put(root2, root1);
                rank.put(root1, rank1 + 1);
            }
            return true;
        }
    }

    public MSTResult findMST(Graph graph) {
        operationsCount = 0;
        long startTime = System.nanoTime();

        List<Edge> mstEdges = new ArrayList<>();
        int totalCost = 0;

        if (graph.getVertexCount() == 0) {
            return new MSTResult(mstEdges, 0, operationsCount, 0.0);
        }

        // Sort all edges by weight
        List<Edge> sortedEdges = new ArrayList<>(graph.getEdges());
        sortedEdges.sort(Edge::compareTo);
        operationsCount += sortedEdges.size() * Math.log(sortedEdges.size()); // Sorting complexity

        UnionFind uf = new UnionFind(graph.getVertices());
        operationsCount += graph.getVertexCount(); // Initialization of Union-Find

        for (Edge edge : sortedEdges) {
            operationsCount++; // Iteration

            String from = edge.getFrom();
            String to = edge.getTo();

            // Count find operations
            String root1 = uf.find(from);
            String root2 = uf.find(to);
            operationsCount += 2; // Two find operations

            if (!root1.equals(root2)) {
                operationsCount++; // Comparison
                mstEdges.add(edge);
                totalCost += edge.getWeight();
                uf.union(from, to);
                operationsCount += 2; // Union operation counting

                // Stop if we have V-1 edges
                if (mstEdges.size() == graph.getVertexCount() - 1) {
                    operationsCount++; // Comparison
                    break;
                }
            } else {
                operationsCount++; // Comparison
            }
        }

        long endTime = System.nanoTime();
        double executionTimeMs = (endTime - startTime) / 1_000_000.0;

        return new MSTResult(mstEdges, totalCost, operationsCount, executionTimeMs);
    }

    public long getOperationsCount() {
        return operationsCount;
    }
}

