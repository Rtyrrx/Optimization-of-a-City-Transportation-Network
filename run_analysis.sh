#!/bin/bash

# City Transportation Network - Comprehensive Build and Run Script

echo "=========================================="
echo "City Transportation Network MST Analysis"
echo "Comprehensive Testing with Multiple Datasets"
echo "=========================================="

# Step 1: Clean and build
echo ""
echo "Step 1: Building project with Maven..."
mvn clean compile

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✓ Build successful!"

# Step 2: Run tests
echo ""
echo "Step 2: Running automated tests..."
mvn test

if [ $? -ne 0 ]; then
    echo "⚠ Some tests failed!"
else
    echo "✓ All tests passed!"
fi

# Step 3: Run main program with primary dataset (input.json)
echo ""
echo "============================================================"
echo "Step 3: Running MST analysis with PRIMARY dataset (input.json)..."
echo "============================================================"
mvn exec:java

if [ $? -ne 0 ]; then
    echo "❌ Primary dataset analysis failed!"
    exit 1
fi

# Backup primary results
echo ""
echo "Backing up primary dataset results..."
cp output.json output_primary.json

# Step 4: Run with additional test datasets
echo ""
echo "============================================================"
echo "Step 4: Running MST analysis with ADDITIONAL dataset (test_datasets.json)..."
echo "============================================================"

# Backup original input.json
cp input.json input_original_backup.json

# Copy test_datasets.json to input.json
cp test_datasets.json input.json

# Run analysis on test datasets
mvn exec:java

if [ $? -ne 0 ]; then
    echo "❌ Test dataset analysis failed!"
    # Restore original input
    mv input_original_backup.json input.json
    exit 1
fi

# Backup test dataset results
cp output.json output_test_datasets.json

# Restore original input.json
mv input_original_backup.json input.json

echo ""
echo "✓ Both dataset analyses completed successfully!"

# Step 5: Generate visualizations for primary dataset
echo ""
echo "============================================================"
echo "Step 5: Generating complexity visualizations..."
echo "============================================================"

# Generate visualizations for primary dataset
cp output_primary.json output.json
python3 visualize_complexity.py

if [ $? -ne 0 ]; then
    echo "⚠ Python visualization failed for primary dataset."
    echo "  Make sure matplotlib and numpy are installed: pip install matplotlib numpy"
else
    echo "✓ Primary dataset visualizations generated successfully!"
    # Rename plots folder
    rm -rf analysis_plots_primary
    mv analysis_plots analysis_plots_primary
fi

# Generate visualizations for test dataset
echo ""
echo "Generating visualizations for test dataset..."
cp output_test_datasets.json output.json
python3 visualize_complexity.py

if [ $? -ne 0 ]; then
    echo "⚠ Python visualization failed for test dataset."
else
    echo "✓ Test dataset visualizations generated successfully!"
    # Rename plots folder
    rm -rf analysis_plots_test
    mv analysis_plots analysis_plots_test
fi

# Restore primary output as default
cp output_primary.json output.json

# Step 6: Generate combined summary report
echo ""
echo "============================================================"
echo "Step 6: Generating combined summary report..."
echo "============================================================"
python3 generate_combined_report.py

if [ $? -ne 0 ]; then
    echo "⚠ Combined report generation skipped (script may not exist yet)"
else
    echo "✓ Combined report generated successfully!"
fi

echo ""
echo "=========================================="
echo "✓ COMPREHENSIVE ANALYSIS COMPLETE!"
echo "=========================================="
echo ""
echo "Results Summary:"
echo "  - Primary dataset results: output_primary.json"
echo "  - Test dataset results: output_test_datasets.json"
echo "  - Current output: output.json"
echo "  - Primary visualizations: analysis_plots_primary/"
echo "  - Test visualizations: analysis_plots_test/"
echo "  - Test results: target/surefire-reports/"
echo ""
echo "Total graphs analyzed: 30 (15 primary + 15 test)"
echo ""
echo "Files generated:"
echo "  [Primary Dataset - 15 graphs, IDs 1-15]"
echo "  - output_primary.json"
echo "  - analysis_plots_primary/operations_vs_vertices.png"
echo "  - analysis_plots_primary/time_vs_vertices.png"
echo "  - analysis_plots_primary/operations_comparison.png"
echo "  - analysis_plots_primary/time_comparison.png"
echo "  - analysis_plots_primary/density_analysis.png"
echo "  - analysis_plots_primary/complexity_verification.png"
echo "  - analysis_plots_primary/summary_table.png"
echo ""
echo "  [Test Dataset - 15 graphs, IDs 101-115]"
echo "  - output_test_datasets.json"
echo "  - analysis_plots_test/operations_vs_vertices.png"
echo "  - analysis_plots_test/time_vs_vertices.png"
echo "  - analysis_plots_test/operations_comparison.png"
echo "  - analysis_plots_test/time_comparison.png"
echo "  - analysis_plots_test/density_analysis.png"
echo "  - analysis_plots_test/complexity_verification.png"
echo "  - analysis_plots_test/summary_table.png"
echo ""
echo "Next steps:"
echo "  1. Review both output JSON files for detailed MST results"
echo "  2. Check both analysis_plots folders for complexity graphs"
echo "  3. Compare performance across 30 different graph configurations"
echo "  4. Read README.md for complete analysis"
echo "  5. Commit and push to GitHub"
echo ""
