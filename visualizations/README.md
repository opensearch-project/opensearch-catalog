# Visualization Catalog

The Visualization Catalog is a central repository for organizing and sharing visualizations used in integrations developed using the standard SS4O framework.
This catalog aims to eliminate duplication of effort by providing a comprehensive collection of commonly applicable visualizations across multiple contexts.

## Problem

As we continue to develop more integrations using standard SS4O, we often encounter overlapping visualization functionality.
For example, many integrations involving an http component may benefit from a "Status codes over time" visualization.
However, without a centralized location for visualizations, developers end up reinventing the wheel, resulting in redundancy and inefficiency.

## Solution

The solution to this problem is the Visualization Catalog, which serves as a directory within this repository.
It allows integration developers to easily find and utilize visualizations that are relevant to their data.
By sharing visualizations in one place, we promote collaboration and reduce duplication of effort.

## Tasks

- [X] Organize Existing Visualizations: Create a new folder within the repository dedicated to the Visualization Catalog. Optionally, structure the visualizations by component to facilitate searchability.
- [ ] Documentation and Guidelines: Provide comprehensive documentation on developing visualizations, explaining the major types and how different fields work. This will serve as a guide for integration developers looking to contribute their own visualizations to the catalog.
- [ ] Enhance the CLI Tool: Extend the CLI tool introduced in #31 (implemented via #32) to analyze visualizations and determine the types of data they can work with. This feature will enable individual visualizations to be checked for compatibility with the standard schema.
- [ ] Search Functionality: Improve the CLI tool by adding search functionality. This enhancement will enable users to quickly find visualizations based on their specific requirements.
- [ ] Automated Dashboard Compilation: Enhance the CLI tool with the capability to automatically compile a list of visualizations into a dashboard. While this feature may be complex, its core objective is to generate a Saved Object file that can be imported into OpenSearch Dashboards.
- [ ] Advanced Catalog API: Consider extending the functionality of the Visualization Catalog to an API with more advanced features. However, this step is optional and should be evaluated based on project demand and feasibility.

## Current Visualizations

The list of visualizations is maintained in [index.yml](index.yml).
The format is still experimental, and may be subject to change in the future.
