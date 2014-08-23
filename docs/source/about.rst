.. APS Data Exchange toolbox

===================
About Data Exchange
===================

Data Exchange is a simple data model that is designed to interface, or "exchange" data among different instruments, and to enable sharing of data analysis tools. Its implementation uses the Heirarchical Data Format (HDF5), a widely used and supported storage format for scientific data.

The Data Exchange definition is highly simplified and focuses on technique rather than instrument descriptions, and on provenance for tracking analysis steps and results. It provides standardization for metadata and the core acquired or analyzed data arrays, while also allowing flexibility for technique or even individual instrument variations.

The key principle of Data Exchange is that for each experimental technique, there is often one particular set of data array that an analysis or visualization program, or researcher will want to access. For example, in X-ray tomography this may be a series of normalized projections or a series of raw projections, followed by white and dark fields arrays.

Data Exchange definition is also set to maximize both the future extensibility of a file to meet evolving data acquisition schemes and data analysis tools, and to improve human readability via h5dump or HDFView so that one can manually examine and understand the file content without access to the computer code used to write it.

This key array, or set of arrays, is placed into an HDF5 group called "exchange" for easy identification.


