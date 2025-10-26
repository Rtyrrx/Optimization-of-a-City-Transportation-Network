import java.util.*;

public class PrimAlgorithm {
    private long operationsCount;

    public MSTResult findMST(Graph graph) {
        operationsCount = 0;
        long startTime = System.nanoTime();

        List<Edge> mstEdges = new ArrayList<>();
        Set<String> visited = new HashSet<>();
        PriorityQueue<Edge> priorityQueue = new PriorityQueue<>();

        if (graph.getVertexCount() == 0) {
            return new MSTResult(mstEdges, 0, operationsCount, 0.0);
        }

        // Start from the first vertex
        String startVertex = graph.getVertices().iterator().next();
        visited.add(startVertex);
        operationsCount++; // Adding to visited set

        // Add all edges from start vertex to priority queue
        for (Edge edge : graph.getAdjacentEdges(startVertex)) {
            priorityQueue.offer(edge);
            operationsCount++; // Queue insertion
        }

        int totalCost = 0;

        while (!priorityQueue.isEmpty() && visited.size() < graph.getVertexCount()) {
            Edge currentEdge = priorityQueue.poll();
            operationsCount++; // Queue removal

            String from = currentEdge.getFrom();
            String to = currentEdge.getTo();
            operationsCount++; // Comparison operation

            // Skip if both vertices are already visited
            if (visited.contains(from) && visited.contains(to)) {
                operationsCount++; // Set lookup operations
                continue;
            }

            // Determine which vertex is new
            String newVertex = visited.contains(from) ? to : from;
            operationsCount++; // Set lookup and conditional

            if (!visited.contains(newVertex)) {
                operationsCount++; // Set lookup
                visited.add(newVertex);
                mstEdges.add(currentEdge);
                totalCost += currentEdge.getWeight();
                operationsCount += 3; // Add to visited, add to MST, addition operation

                // Add all edges from new vertex
                for (Edge edge : graph.getAdjacentEdges(newVertex)) {
                    operationsCount++; // Iteration
                    String neighbor = edge.getTo();
                    if (!visited.contains(neighbor)) {
                        operationsCount++; // Set lookup
                        priorityQueue.offer(edge);
                        operationsCount++; // Queue insertion
                    } else {
                        operationsCount++; // Set lookup
                    }
                }
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

