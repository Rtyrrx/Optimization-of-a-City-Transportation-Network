@echo off
REM City Transportation Network - Comprehensive Build and Run Script (Windows)

echo ==========================================
echo City Transportation Network MST Analysis
echo Comprehensive Testing with Multiple Datasets
echo ==========================================

REM Step 1: Clean and build
echo.
echo Step 1: Building project with Maven...
call mvn clean compile

if %ERRORLEVEL% NEQ 0 (
    echo X Build failed!
    exit /b 1
)

echo + Build successful!

REM Step 2: Run tests
echo.
echo Step 2: Running automated tests...
call mvn test

if %ERRORLEVEL% NEQ 0 (
    echo ! Some tests failed!
) else (
    echo + All tests passed!
)

REM Step 3: Run main program with primary dataset (input.json)
echo.
echo ============================================================
echo Step 3: Running MST analysis with PRIMARY dataset (input.json)...
echo ============================================================
call mvn exec:java

if %ERRORLEVEL% NEQ 0 (
    echo X Primary dataset analysis failed!
    exit /b 1
)

REM Backup primary results
echo.
echo Backing up primary dataset results...
copy output.json output_primary.json

REM Step 4: Run with additional test datasets
echo.
echo ============================================================
echo Step 4: Running MST analysis with ADDITIONAL dataset (test_datasets.json)...
echo ============================================================

REM Backup original input.json
copy input.json input_original_backup.json

REM Copy test_datasets.json to input.json
copy test_datasets.json input.json

REM Run analysis on test datasets
call mvn exec:java

if %ERRORLEVEL% NEQ 0 (
    echo X Test dataset analysis failed!
    REM Restore original input
    move /y input_original_backup.json input.json
    exit /b 1
)

REM Backup test dataset results
copy output.json output_test_datasets.json

REM Restore original input.json
move /y input_original_backup.json input.json

echo.
echo + Both dataset analyses completed successfully!

REM Step 5: Generate visualizations for primary dataset
echo.
echo ============================================================
echo Step 5: Generating complexity visualizations...
echo ============================================================

REM Generate visualizations for primary dataset
copy output_primary.json output.json
python visualize_complexity.py

if %ERRORLEVEL% NEQ 0 (
    echo ! Python visualization failed for primary dataset.
    echo   Make sure matplotlib and numpy are installed: pip install matplotlib numpy
) else (
    echo + Primary dataset visualizations generated successfully!
    REM Rename plots folder
    if exist analysis_plots_primary rmdir /s /q analysis_plots_primary
    move analysis_plots analysis_plots_primary
)

REM Generate visualizations for test dataset
echo.
echo Generating visualizations for test dataset...
copy output_test_datasets.json output.json
python visualize_complexity.py

if %ERRORLEVEL% NEQ 0 (
    echo ! Python visualization failed for test dataset.
) else (
    echo + Test dataset visualizations generated successfully!
    REM Rename plots folder
    if exist analysis_plots_test rmdir /s /q analysis_plots_test
    move analysis_plots analysis_plots_test
)

REM Restore primary output as default
copy output_primary.json output.json

REM Step 6: Generate combined summary report
echo.
echo ============================================================
echo Step 6: Generating combined summary report...
echo ============================================================
python generate_combined_report.py

if %ERRORLEVEL% NEQ 0 (
    echo ! Combined report generation skipped (script may not exist yet)
) else (
    echo + Combined report generated successfully!
)

echo.
echo ==========================================
echo + COMPREHENSIVE ANALYSIS COMPLETE!
echo ==========================================
echo.
echo Results Summary:
echo   - Primary dataset results: output_primary.json
echo   - Test dataset results: output_test_datasets.json
echo   - Current output: output.json
echo   - Primary visualizations: analysis_plots_primary\
echo   - Test visualizations: analysis_plots_test\
echo   - Test results: target\surefire-reports\
echo.
echo Total graphs analyzed: 30 (15 primary + 15 test)
echo.
echo Files generated:
echo   [Primary Dataset - 15 graphs, IDs 1-15]
echo   - output_primary.json
echo   - analysis_plots_primary\operations_vs_vertices.png
echo   - analysis_plots_primary\time_vs_vertices.png
echo   - analysis_plots_primary\operations_comparison.png
echo   - analysis_plots_primary\time_comparison.png
echo   - analysis_plots_primary\density_analysis.png
echo   - analysis_plots_primary\complexity_verification.png
echo   - analysis_plots_primary\summary_table.png
echo.
echo   [Test Dataset - 15 graphs, IDs 101-115]
echo   - output_test_datasets.json
echo   - analysis_plots_test\operations_vs_vertices.png
echo   - analysis_plots_test\time_vs_vertices.png
echo   - analysis_plots_test\operations_comparison.png
echo   - analysis_plots_test\time_comparison.png
echo   - analysis_plots_test\density_analysis.png
echo   - analysis_plots_test\complexity_verification.png
echo   - analysis_plots_test\summary_table.png
echo.
echo Next steps:
echo   1. Review both output JSON files for detailed MST results
echo   2. Check both analysis_plots folders for complexity graphs
echo   3. Compare performance across 30 different graph configurations
echo   4. Read README.md for complete analysis
echo   5. Commit and push to GitHub
echo.
pause
# Compiled class files
*.class

# Log files
*.log

# Package Files
*.jar
*.war
*.nar
*.ear
*.zip
*.tar.gz
*.rar

# Maven
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties
dependency-reduced-pom.xml
buildNumber.properties
.mvn/timing.properties
.mvn/wrapper/maven-wrapper.jar

# IntelliJ IDEA
.idea/
*.iws
*.iml
*.ipr
out/

# Eclipse
.classpath
.project
.settings/
bin/

# VS Code
.vscode/

# MacOS
.DS_Store

# Windows
Thumbs.db
ehthumbs.db
Desktop.ini

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Jupyter Notebook
.ipynb_checkpoints

# Analysis output (keep structure, ignore generated plots during development)
# Uncomment if you want to ignore generated plots
# analysis_plots/*.png

# Temporary files
*.tmp
*.bak
*.swp
*~
