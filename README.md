This document describes usage of Grapher tool

## Pre-requisites
 - Internet to download pip packages
 - Install the packages:
   > pip install -r requirements.txt

## Usage
 - Modify configuration file
 - Execute below script to create graphs:
   > python grapher.py -c <config-file>

## Configuration Manual
 - __input:__ _input csv filename_
 - __output:__ _output filename. If not provided, it will be same as input_
 - __plot_main_title:__ _plot title (in double quotes)_
 - __plot_sub_title:__ _plot sub title (in double quotes)_
 - __primary_x:__ _x-axis properties_
   - __axis:__ _csv column containing x-axis values. Ex:'users'_
   - __title:__ _axis title. Options: auto/custom_name. Recommended: auto_
   - __ticks:__ _axis ticks. Options: auto/csv-column-containing-x-tick-values/list-of-values. Recommended: auto_
   - __rotation:__ _ticks rotation in degrees. Recommended: 0_
   - __font_size:__ _axis title font size. Recommended: 12_
 - __primary_y:__ _left-y-axis properties_
 - __secondary_y:__ _right-y-axis properties_
   - __axes:__ _csv columns list containing y-axis values. Ex:['cpu','mem']_
   - __labels:__ _alias names for above axes. Options: auto/custom_list_
   - __graph_type:__ _type of plot. Options: bar/line_
   - __title:__ _axis title. Options: auto/custom_name_
   - __font_size:__ _axis title font size. Recommended: 12_
   - __ticks:__ _axis ticks. Options: auto/csv-column-containing-y-tick-values/list-of-values. Recommended: auto_
   - __colors:__ _custom plot colors. Options: auto/list-of-values. Recommended: auto_
   - __limits:__ _y-axis limits. Options: auto/[y_min,y_max]. Recommended: auto_
 - __line_graph_properties:__ _properties for line graphs_
   - __line_width:__ _width of line plot. Recommended: 2.5_
   - __line_style:__ _line plot styles. Options: '-/--/.-'. For complete list, refer [here](https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html)_
   - __markers:__ _to show point markers. Options: True/False_
   - __marker_style:__ _marker style. Recommended: 'o'. Options: 'o/./*'. For complete list, refer [here](https://matplotlib.org/stable/api/markers_api.html)_
   - __marker_size:__ _Size of marker. Recommended: 3_
 - __data_labels:__ _properties for data labels_
   - __show:__ _show data labels. Options: True/False_
   - __precision:__ _precision for data labels. Recommended: 2_
   - __font_size:__ _font size of data labels. Recommended: 8_
 - __grid:__ _grid properties_
   - __show_x_grid:__ _show x-axis grid. Options: True/False_
   - __primary_y:__ _left-y-axis grid properties_
   - __secondary_y:__ _right-y-axis grid properties_
     - __line_style:__ _grid line styles. Options: '-/--/.-'. For complete list, refer [here](https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html)_
     - __line_width:__ _width of grid lines. Recommended: 0.5_
     - __color:__ _grid color. Recommended: 'grey'_
 - __legend:__ _show legend. Options: True/False_
 - __font_style:__ _font family. Recommended: 'Graphik'_
 - __show_tick_limits:__ _show y-axes min and max ticks. Options: True/False_
 - __tick_size:__ _font size of ticks. Recommended: 10_
 - __main_title_size:__ _plot main title fontsize. Recommended: 16_
 - __sub_title_size:__ _plot sub title fontsize. Recommended: 14_
 - __plot_size_in_inches:__ _output plot dimensions (in inches) as [length, width]. Recommended: [10, 6]_
 - __quality_in_dpi:__ _output image quality (higher value indicates better quality). Recommended: 100_
