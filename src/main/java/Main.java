import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;
import java.util.logging.Level;

public class Main {
    private static final Logger LOGGER = Logger.getLogger(Main.class.getName());

    public static void main(String[] args) {
        try {
            System.out.println("=== City Transportation Network - MST Analysis ===\n");

            // Load graphs from JSON
            String inputFile = "input.json";
            List<Graph> graphs = GraphDataLoader.loadGraphsFromJson(inputFile);
            System.out.println("Loaded " + graphs.size() + " graph(s) from " + inputFile + "\n");

            List<MSTResult> primResults = new ArrayList<>();
            List<MSTResult> kruskalResults = new ArrayList<>();

            // Process each graph
            for (Graph graph : graphs) {
                System.out.println("Processing Graph " + graph.getGraphId() + ":");
                System.out.println("  Vertices: " + graph.getVertexCount());
                System.out.println("  Edges: " + graph.getEdgeCount());
                System.out.println("  Connected: " + graph.isConnected());

                // Run Prim's Algorithm
                System.out.println("\n--- Prim's Algorithm ---");
                PrimAlgorithm prim = new PrimAlgorithm();
                MSTResult primResult = prim.findMST(graph);
                primResults.add(primResult);
                printResult(primResult);

                // Run Kruskal's Algorithm
                System.out.println("\n--- Kruskal's Algorithm ---");
                KruskalAlgorithm kruskal = new KruskalAlgorithm();
                MSTResult kruskalResult = kruskal.findMST(graph);
                kruskalResults.add(kruskalResult);
                printResult(kruskalResult);

                // Comparison
                System.out.println("\n--- Comparison ---");
                System.out.println("  Total Cost Match: " + (primResult.getTotalCost() == kruskalResult.getTotalCost()));
                System.out.println("  Prim Operations: " + primResult.getOperationsCount());
                System.out.println("  Kruskal Operations: " + kruskalResult.getOperationsCount());
                System.out.println("  Prim Time: " + String.format("%.2f", primResult.getExecutionTimeMs()) + " ms");
                System.out.println("  Kruskal Time: " + String.format("%.2f", kruskalResult.getExecutionTimeMs()) + " ms");
                System.out.println("\n" + "=".repeat(60) + "\n");
            }

            // Save results to JSON
            String outputFile = "output.json";
            GraphDataLoader.saveResultsToJson(graphs, primResults, kruskalResults, outputFile);
            System.out.println("Results saved to " + outputFile);

        } catch (IOException e) {
            LOGGER.log(Level.SEVERE, "Error processing graphs: " + e.getMessage(), e);
            System.err.println("Error: " + e.getMessage());
        }
    }

    private static void printResult(MSTResult result) {
        System.out.println("  MST Edges:");
        for (Edge edge : result.getMstEdges()) {
            System.out.println("    " + edge.getFrom() + " -> " + edge.getTo() +
                             " (weight: " + edge.getWeight() + ")");
        }
        System.out.println("  Total Cost: " + result.getTotalCost());
        System.out.println("  Operations: " + result.getOperationsCount());
        System.out.println("  Execution Time: " + String.format("%.2f", result.getExecutionTimeMs()) + " ms");
    }
}
