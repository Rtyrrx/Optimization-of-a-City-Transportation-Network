import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

@DisplayName("MST Algorithm Tests")
public class MSTAlgorithmTest {

    private PrimAlgorithm prim;
    private KruskalAlgorithm kruskal;

    @BeforeEach
    public void setUp() {
        prim = new PrimAlgorithm();
        kruskal = new KruskalAlgorithm();
    }

    @Test
    @DisplayName("Test 1: Small graph correctness")
    public void testSmallGraphCorrectness() {
        Graph graph = createSmallGraph();

        MSTResult primResult = prim.findMST(graph);
        MSTResult kruskalResult = kruskal.findMST(graph);

        // Both should have same total cost
        assertEquals(primResult.getTotalCost(), kruskalResult.getTotalCost(),
                    "Prim and Kruskal should produce same total cost");

        // Both should have V-1 edges
        assertEquals(graph.getVertexCount() - 1, primResult.getMstEdges().size(),
                    "Prim MST should have V-1 edges");
        assertEquals(graph.getVertexCount() - 1, kruskalResult.getMstEdges().size(),
                    "Kruskal MST should have V-1 edges");
    }

    @Test
    @DisplayName("Test 2: MST has no cycles")
    public void testMSTIsAcyclic() {
        Graph graph = createSmallGraph();

        MSTResult primResult = prim.findMST(graph);
        MSTResult kruskalResult = kruskal.findMST(graph);

        assertFalse(hasCycle(primResult.getMstEdges(), graph.getVertices()),
                   "Prim MST should be acyclic");
        assertFalse(hasCycle(kruskalResult.getMstEdges(), graph.getVertices()),
                   "Kruskal MST should be acyclic");
    }

    @Test
    @DisplayName("Test 3: MST connects all vertices")
    public void testMSTConnectsAllVertices() {
        Graph graph = createSmallGraph();

        MSTResult primResult = prim.findMST(graph);
        MSTResult kruskalResult = kruskal.findMST(graph);

        assertTrue(isConnected(primResult.getMstEdges(), graph.getVertices()),
                  "Prim MST should connect all vertices");
        assertTrue(isConnected(kruskalResult.getMstEdges(), graph.getVertices()),
                  "Kruskal MST should connect all vertices");
    }

    @Test
    @DisplayName("Test 4: Expected total cost for known graph")
    public void testKnownGraphCost() {
        Graph graph = createSmallGraph();

        MSTResult primResult = prim.findMST(graph);
        MSTResult kruskalResult = kruskal.findMST(graph);

        // For the small graph (square), MST cost should be 6
        int expectedCost = 6;
        assertEquals(expectedCost, primResult.getTotalCost(),
                    "Prim should find MST with cost 6");
        assertEquals(expectedCost, kruskalResult.getTotalCost(),
                    "Kruskal should find MST with cost 6");
    }

    @Test
    @DisplayName("Test 5: Medium graph correctness")
    public void testMediumGraphCorrectness() {
        Graph graph = createMediumGraph();

        MSTResult primResult = prim.findMST(graph);
        MSTResult kruskalResult = kruskal.findMST(graph);

        assertEquals(primResult.getTotalCost(), kruskalResult.getTotalCost(),
                    "Both algorithms should produce same cost for medium graph");
        assertEquals(graph.getVertexCount() - 1, primResult.getMstEdges().size(),
                    "Should have V-1 edges");
    }

    @Test
    @DisplayName("Test 6: Empty graph handling")
    public void testEmptyGraph() {
        Graph graph = new Graph(999);

        MSTResult primResult = prim.findMST(graph);
        MSTResult kruskalResult = kruskal.findMST(graph);

        assertEquals(0, primResult.getTotalCost(), "Empty graph should have cost 0");
        assertEquals(0, kruskalResult.getTotalCost(), "Empty graph should have cost 0");
        assertEquals(0, primResult.getMstEdges().size(), "Empty graph should have 0 edges");
        assertEquals(0, kruskalResult.getMstEdges().size(), "Empty graph should have 0 edges");
    }

    @Test
    @DisplayName("Test 7: Single vertex graph")
    public void testSingleVertexGraph() {
        Graph graph = new Graph(998);
        graph.addVertex("A");

        MSTResult primResult = prim.findMST(graph);
        MSTResult kruskalResult = kruskal.findMST(graph);

        assertEquals(0, primResult.getTotalCost(), "Single vertex should have cost 0");
        assertEquals(0, kruskalResult.getTotalCost(), "Single vertex should have cost 0");
        assertEquals(0, primResult.getMstEdges().size(), "Single vertex should have 0 edges");
    }

    @Test
    @DisplayName("Test 8: Operations count is positive")
    public void testOperationsCountPositive() {
        Graph graph = createSmallGraph();

        MSTResult primResult = prim.findMST(graph);
        MSTResult kruskalResult = kruskal.findMST(graph);

        assertTrue(primResult.getOperationsCount() >= 0,
                  "Prim operations count should be non-negative");
        assertTrue(kruskalResult.getOperationsCount() >= 0,
                  "Kruskal operations count should be non-negative");
    }

    @Test
    @DisplayName("Test 9: Execution time is positive")
    public void testExecutionTimePositive() {
        Graph graph = createSmallGraph();

        MSTResult primResult = prim.findMST(graph);
        MSTResult kruskalResult = kruskal.findMST(graph);

        assertTrue(primResult.getExecutionTimeMs() >= 0,
                  "Prim execution time should be non-negative");
        assertTrue(kruskalResult.getExecutionTimeMs() >= 0,
                  "Kruskal execution time should be non-negative");
    }

    @Test
    @DisplayName("Test 10: Reproducibility - same input produces same output")
    public void testReproducibility() {
        Graph graph = createSmallGraph();

        MSTResult primResult1 = prim.findMST(graph);
        MSTResult primResult2 = prim.findMST(graph);

        assertEquals(primResult1.getTotalCost(), primResult2.getTotalCost(),
                    "Same graph should produce same MST cost");
        assertEquals(primResult1.getMstEdges().size(), primResult2.getMstEdges().size(),
                    "Same graph should produce same number of edges");
    }

    @Test
    @DisplayName("Test 11: Large graph performance")
    public void testLargeGraphPerformance() {
        Graph graph = createLargeGraph();

        MSTResult primResult = prim.findMST(graph);
        MSTResult kruskalResult = kruskal.findMST(graph);

        assertEquals(primResult.getTotalCost(), kruskalResult.getTotalCost(),
                    "Both algorithms should produce same cost for large graph");
        assertEquals(graph.getVertexCount() - 1, primResult.getMstEdges().size(),
                    "Large graph should have V-1 edges");

        // Performance should be reasonable (less than 1 second for 30 vertices)
        assertTrue(primResult.getExecutionTimeMs() < 1000,
                  "Prim should complete in reasonable time");
        assertTrue(kruskalResult.getExecutionTimeMs() < 1000,
                  "Kruskal should complete in reasonable time");
    }

    // Helper methods

    private Graph createSmallGraph() {
        // Graph 2 from input.json
        Graph graph = new Graph(2);
        graph.addEdge("A", "B", 1);
        graph.addEdge("A", "C", 4);
        graph.addEdge("B", "C", 2);
        graph.addEdge("C", "D", 3);
        graph.addEdge("B", "D", 5);
        return graph;
    }

    private Graph createMediumGraph() {
        Graph graph = new Graph(10);

        // Create a connected graph with 15 edges
        graph.addEdge("A", "B", 4);
        graph.addEdge("A", "C", 3);
        graph.addEdge("B", "C", 2);
        graph.addEdge("B", "D", 5);
        graph.addEdge("C", "D", 7);
        graph.addEdge("C", "E", 8);
        graph.addEdge("D", "E", 6);
        graph.addEdge("E", "F", 2);
        graph.addEdge("F", "G", 3);
        graph.addEdge("G", "H", 1);
        graph.addEdge("H", "I", 4);
        graph.addEdge("I", "J", 2);
        graph.addEdge("A", "F", 10);
        graph.addEdge("D", "H", 9);
        graph.addEdge("E", "J", 11);

        return graph;
    }

    private Graph createLargeGraph() {
        Graph graph = new Graph(30);

        // Create 30 vertices
        for (int i = 0; i < 30; i++) {
            graph.addVertex("V" + i);
        }

        // Create a connected graph with random edges
        Random random = new Random(42); // Fixed seed for reproducibility
        for (int i = 0; i < 29; i++) {
            graph.addEdge("V" + i, "V" + (i + 1), random.nextInt(20) + 1);
        }

        // Add additional edges for density
        for (int i = 0; i < 50; i++) {
            int v1 = random.nextInt(30);
            int v2 = random.nextInt(30);
            if (v1 != v2) {
                graph.addEdge("V" + v1, "V" + v2, random.nextInt(20) + 1);
            }
        }

        return graph;
    }

    private boolean hasCycle(List<Edge> edges, Set<String> vertices) {
        Map<String, String> parent = new HashMap<>();
        for (String v : vertices) {
            parent.put(v, v);
        }

        for (Edge edge : edges) {
            String root1 = find(parent, edge.getFrom());
            String root2 = find(parent, edge.getTo());

            if (root1.equals(root2)) {
                return true; // Cycle detected
            }
            parent.put(root1, root2);
        }
        return false;
    }

    private String find(Map<String, String> parent, String vertex) {
        if (!parent.get(vertex).equals(vertex)) {
            parent.put(vertex, find(parent, parent.get(vertex)));
        }
        return parent.get(vertex);
    }

    private boolean isConnected(List<Edge> edges, Set<String> vertices) {
        if (vertices.isEmpty()) return true;

        Map<String, List<String>> adj = new HashMap<>();
        for (String v : vertices) {
            adj.put(v, new ArrayList<>());
        }

        for (Edge edge : edges) {
            adj.get(edge.getFrom()).add(edge.getTo());
            adj.get(edge.getTo()).add(edge.getFrom());
        }

        Set<String> visited = new HashSet<>();
        Queue<String> queue = new LinkedList<>();
        String start = vertices.iterator().next();
        queue.offer(start);
        visited.add(start);

        while (!queue.isEmpty()) {
            String current = queue.poll();
            for (String neighbor : adj.get(current)) {
                if (!visited.contains(neighbor)) {
                    visited.add(neighbor);
                    queue.offer(neighbor);
                }
            }
        }

        return visited.size() == vertices.size();
    }
}
