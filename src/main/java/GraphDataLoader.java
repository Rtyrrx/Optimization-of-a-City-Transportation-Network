import com.google.gson.*;
import java.io.*;
import java.util.*;

public class GraphDataLoader {

    public static List<Graph> loadGraphsFromJson(String filename) throws IOException {
        List<Graph> graphs = new ArrayList<>();

        try (Reader reader = new FileReader(filename)) {
            JsonObject jsonObject = JsonParser.parseReader(reader).getAsJsonObject();
            JsonArray graphsArray = jsonObject.getAsJsonArray("graphs");

            for (JsonElement graphElement : graphsArray) {
                JsonObject graphObj = graphElement.getAsJsonObject();
                int id = graphObj.get("id").getAsInt();

                Graph graph = new Graph(id);

                // Add vertices
                JsonArray nodesArray = graphObj.getAsJsonArray("nodes");
                for (JsonElement nodeElement : nodesArray) {
                    graph.addVertex(nodeElement.getAsString());
                }

                // Add edges
                JsonArray edgesArray = graphObj.getAsJsonArray("edges");
                for (JsonElement edgeElement : edgesArray) {
                    JsonObject edgeObj = edgeElement.getAsJsonObject();
                    String from = edgeObj.get("from").getAsString();
                    String to = edgeObj.get("to").getAsString();
                    int weight = edgeObj.get("weight").getAsInt();
                    graph.addEdge(from, to, weight);
                }

                graphs.add(graph);
            }
        }

        return graphs;
    }

    public static void saveResultsToJson(List<Graph> graphs,
                                        List<MSTResult> primResults,
                                        List<MSTResult> kruskalResults,
                                        String filename) throws IOException {
        JsonObject root = new JsonObject();
        JsonArray resultsArray = new JsonArray();

        for (int i = 0; i < graphs.size(); i++) {
            Graph graph = graphs.get(i);
            MSTResult primResult = primResults.get(i);
            MSTResult kruskalResult = kruskalResults.get(i);

            JsonObject resultObj = new JsonObject();
            resultObj.addProperty("graph_id", graph.getGraphId());

            // Input stats
            JsonObject inputStats = new JsonObject();
            inputStats.addProperty("vertices", graph.getVertexCount());
            inputStats.addProperty("edges", graph.getEdgeCount());
            resultObj.add("input_stats", inputStats);

            // Prim results
            JsonObject primObj = createAlgorithmResult(primResult);
            resultObj.add("prim", primObj);

            // Kruskal results
            JsonObject kruskalObj = createAlgorithmResult(kruskalResult);
            resultObj.add("kruskal", kruskalObj);

            resultsArray.add(resultObj);
        }

        root.add("results", resultsArray);

        // Write to file with pretty printing
        try (Writer writer = new FileWriter(filename)) {
            Gson gson = new GsonBuilder().setPrettyPrinting().create();
            gson.toJson(root, writer);
        }
    }

    private static JsonObject createAlgorithmResult(MSTResult result) {
        JsonObject obj = new JsonObject();

        // MST edges
        JsonArray edgesArray = new JsonArray();
        for (Edge edge : result.getMstEdges()) {
            JsonObject edgeObj = new JsonObject();
            edgeObj.addProperty("from", edge.getFrom());
            edgeObj.addProperty("to", edge.getTo());
            edgeObj.addProperty("weight", edge.getWeight());
            edgesArray.add(edgeObj);
        }
        obj.add("mst_edges", edgesArray);

        obj.addProperty("total_cost", result.getTotalCost());
        obj.addProperty("operations_count", result.getOperationsCount());
        obj.addProperty("execution_time_ms", Math.round(result.getExecutionTimeMs() * 100.0) / 100.0);

        return obj;
    }
}

