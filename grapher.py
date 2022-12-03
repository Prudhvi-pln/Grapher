# This script plots graphs
__author__ = 'Prudhvi Ch'
__version__ = '1.0'

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import argparse, yaml, yamlordereddictloader
from datetime import datetime


def load_yaml_file(conf_file):
    cfg = {}
    try:
        with open(conf_file, 'r') as yaml_file:
            cfg = yaml.load(yaml_file, Loader = yamlordereddictloader.Loader)

    except yaml.YAMLError as ex:
        print(ex)

    except Exception as ex:
        print(ex)

    return cfg


def logger(msg):
    # log format
    ts = datetime.now().strftime('%F %T')
    BLU = '\033[1;34m'
    RED = '\033[0;31m'
    END = '\033[0m'
    log_level = RED if 'ERROR' in msg or 'WARN' in msg else BLU
    print("{}{} {}{}".format(log_level, ts, msg, END))


def validate_config(conf, flag=False):
    if len(config['plot_main_title']) > 0 and len(config['plot_sub_title']) > 0:
        cnt1 = config['plot_main_title'].count('\n')
        cnt2 = config['plot_sub_title'].count('\n')
        if cnt1 > 1 or cnt2 > 0:
            logger('[ERROR] Main title cannot have more than 2 lines, and Sub title cannot have more than 1 line')
            flag = True
    for axis in _axes_:
        if len(conf[axis]['axes']) > 0:
            for p in ['labels', 'colors']:
                if conf[axis][p] != 'auto' and len(conf[axis][p]) != len(conf[axis]['axes']):
                    logger('[ERROR] ' + p.capitalize() + ' and Axes count does not match for: ' + axis)
                    flag = True
            if conf[axis]['limits'] != 'auto':
                if len(conf[axis]['limits']) != 2:
                    logger('[ERROR] Provide both limits for: ' + axis)
                    flag = True
                elif len(conf[axis]['limits']) == 2 and (conf[axis]['limits'][0] > conf[axis]['limits'][1]):
                    logger('[ERROR] Lower limit is higher than Upper limit: ' + axis)
                    flag = True
    if type(conf['plot_size_in_inches']) is not list:
        logger('[ERROR] Provide plot_size_in_inches as list. Ex: [10, 6]')
        flag = True
    else:
        if conf['plot_size_in_inches'][0] < 5 or conf['plot_size_in_inches'][1] < 5:
            logger('[WARN] The plot_size_in_inches provided is below minimum limits of [5, 5]. Your plot may get disfigured!')

    if flag: exit(1)


def get_case(y1_props, y2_props):
    if y1_props['graph_type'] == 'line' and y2_props['graph_type'] == 'bar':
        return 1
    elif y1_props['graph_type'] == 'bar' and y2_props['graph_type'] == 'bar':
        return 2
    elif len(y1_props['axes']) <= 0 and len(y2_props['axes']) > 0:
        return 3
    else:
        return 0


def add_xaxis_props(ax, df, x_props):
    # set x-axis ticks
    ax.set_xticks(df.index)
    if x_props['ticks'] != 'auto':
        if x_props['ticks'] in list(df.columns):
            ax.set_xticklabels(df[x_props['ticks']], rotation=x_props['rotation'])
        else:
            ax.set_xticklabels(x_props['ticks'], rotation=x_props['rotation'])
    else:
        ax.set_xticklabels(df[x_props['axis']], rotation=x_props['rotation'])

    # set x-axis title
    if x_props['title'] == 'auto':
        ax.set_xlabel(x_props['axis'].capitalize(), fontsize=x_props['font_size'])
    else:
        ax.set_xlabel(x_props['title'], fontsize=x_props['font_size'])


def add_yaxis_props(ax, df, y_props):
    y_padding = 1.1

    # set y-axis limits
    if y_props['limits'] != 'auto':
        y_min = y_props['limits'][0]
        y_max = y_props['limits'][1]
    else:
        y_min = 0 if df[y_props['axes']].min().min() >= 0 else (df[y_props['axes']].min().min() * y_padding)
        y_max = df[y_props['axes']].max().max() * y_padding
    y_min = round(y_min, 2)
    y_max = round(y_max, 2)
    ax.set_ylim(y_min, y_max)

    # set y-ticks
    if y_props['ticks'] != 'auto':
        if y_props['ticks'] in list(df.columns):
            ax.set_yticks(df[y_props['ticks']])
        else:
            ax.set_yticks(y_props['ticks'])

    # set upper and lower y-tick labels
    if config['show_tick_limits']:
        tcks = list(ax.get_yticks())
        tck_avg = (tcks[-1] - tcks[-2]) / 4.0
        if (y_max > tcks[-1]):
            tcks.append(y_max)
        else:
            tcks[-1] = y_max
        if tcks[0] > (y_min * 1.05):
            tcks = [y_min] + tcks
        else:
            tcks[0] = y_min
        if (tcks[-1] - tcks[-2]) < tck_avg:
            tcks = tcks[:-2]; tcks.append(y_max)
        ax.set_yticks(tcks)

    # set y-axis title
    lbl = ' & '.join(y.capitalize() for y in y_props['labels']) if y_props['title'] == 'auto' else y_props['title']
    if y_props['title'] == 'auto':
        lbl_key = 'labels' if y_props['labels'] != 'auto' else 'axes'
        lbl = ' & '.join(y.capitalize() for y in y_props[lbl_key])
    else:
        lbl = y_props['title']
    ax.set_ylabel(lbl, fontsize=y_props['font_size'])


def add_grid(ax, grid_props, show_x):
    axes = 'both' if show_x else 'y'
    ax.set_axisbelow(True)
    ax.grid('on', which='major', axis=axes, linestyle=grid_props['line_style'], linewidth = grid_props['line_width'], color=grid_props['color'])


def add_legend(ax, fig, show_legend, lgnd_width_factor=8):
    if not show_legend:
        return 0
    lgnd_max_width = config['plot_size_in_inches'][0] * lgnd_width_factor
    lbls = []
    lgnd_height = []
    # Set Legend labels
    for _ax_, y in zip(fig.axes, _axes_):
        h, l = _ax_.get_legend_handles_labels()
        if config[y]['labels'] == 'auto':
            lbls.extend([ y.capitalize() for y in config[y]['axes'] ])
        elif len(config[y]['axes']) > 0:
            lbls.extend(config[y]['labels'])
        lgnd_height += h
    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    # Put the Legend below current axis
    lgnd_y_pos = (0.1 / config['plot_size_in_inches'][1]) + 0.1
    # Get optimal no. of columns for Legend
    for n in range(len(lbls), 0, -2):
        flag = True
        for sl in [lbls[i:i+n] for i in range(0, len(lbls), n)]:
            if sum([len(i) for i in sl]) > lgnd_max_width:
                flag = False
        if flag:
            break
    lgnd_cols = n
    # Set custom Legend
    ax.legend(lgnd_height, lbls, fontsize=(config['primary_y']['font_size'] - 2), loc='upper center', bbox_to_anchor=(0.5, -lgnd_y_pos), fancybox=True, ncol=lgnd_cols)


def add_title():
    if len(config['plot_sub_title']) > 0:
        cnt = config['plot_main_title'].count('\n') + 1
        title_y_pos = 0.97 if cnt == 1 else 1.0
        plt.suptitle(config['plot_main_title'], fontsize=config['main_title_size'], y=title_y_pos)
        plt.title(config['plot_sub_title'], fontsize=config['sub_title_size'])
    else:
        plt.title(config['plot_main_title'], fontsize=config['main_title_size'])


def add_data_labels(ax, dl_props, type, spacing=5):
    if not dl_props['show']:
        return 0

    if type == 'bar':
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.{}f'.format(dl_props['precision'])), (p.get_x() + p.get_width() / 2., p.get_height()), 
                    xytext=(0, spacing), textcoords='offset points', ha='center', va='bottom', fontsize=dl_props['font_size'])
    else:
        for line in ax.lines:
            for x_value, y_value in zip(line.get_xdata(), line.get_ydata()):
                    ax.annotate(format(y_value, '.{}f'.format(dl_props['precision'])), (x_value, y_value), 
                            xytext=(0, spacing), textcoords='offset points', ha='center', va='bottom', fontsize=dl_props['font_size'])


def add_line_params(params, line_props):
    params.update({
        'lw': line_props['line_width'],
        'linestyle': line_props['line_style']
    })
    # set marker options
    if line_props['markers']:
        params.update({
            'marker': line_props['marker_style'],
            'markersize': line_props['marker_size']
        })

    return params


def add_plot(_ax_, df, y_props, comp_y_props, case, is_secondary=False):
    # return the axis without any changes for below conditions
    if (len(y_props['axes']) <= 0) or (case == 2 and not is_secondary):
        return _ax_

    # set secondary axis
    ax = _ax_.twinx() if (is_secondary and case != 2) else _ax_

    # define options
    params = {
        'ax': ax,
        'kind': y_props['graph_type'],
        'legend': False,
        'fontsize': config['tick_size']
    }

    if case == 2:
        # get only plot columns
        df = df[comp_y_props['axes'] + y_props['axes']]
        params.update({'secondary_y': y_props['axes']})
    else:
        params.update({'y': y_props['axes']})

    # set colors
    if y_props['colors'] == 'auto':
        if case == 2:
            st = 0
            ed = len(y_props['axes']) + len(comp_y_props['axes'])
        else:
            st = len(comp_y_props['axes']) if is_secondary else 0
            ed = st + len(y_props['axes'])
        params.update({'color': color_palette[st:ed]})
    else:
        if case == 2:
            params.update({'color': comp_y_props['colors'] + y_props['colors']})
        else:
            params.update({'color': y_props['colors']})

    # set line options
    if y_props['graph_type'] == 'line':
        params = add_line_params(params, config['line_graph_properties'])

    # add plot
    df.plot(**params)

    return ax


def render_graph(config, input, output):
    # Load data
    _df_ = pd.read_csv(input, sep=',')
    # set font family
    plt.rcParams['font.family'] = config['font_style']

    fig, ax = plt.subplots()
    fig.set_size_inches(config['plot_size_in_inches'])

    # get type of correlation plot
    case = get_case(config['primary_y'], config['secondary_y'])

    # add primary y-axes
    ax1 = add_plot(ax, _df_, config['primary_y'], config['secondary_y'], case)
    # add secondary y-axes
    ax2 = add_plot(ax1, _df_, config['secondary_y'], config['primary_y'], case, True)

    # special cases
    if case == 1:
        # case-1: re-order the plots if y1 is line, and y2 is bar
        ax1.set_zorder(2)
        ax1.set_facecolor('none')
        ax2.set_zorder(1)
    elif case == 3:
        # case-3: hide y1 axis if y1 is empty
        ax1.get_yaxis().set_visible(False)

    # set x-axis props
    add_xaxis_props(ax, _df_, config['primary_x'])

    for _ax_, y in zip(fig.axes, _axes_):
        if len(config[y]['axes']) > 0:
            # set y-axis props
            add_yaxis_props(_ax_, _df_, config[y])
            # set grid options
            add_grid(_ax_, config['grid'][y], config['grid']['show_x_grid'])
            # set data labels
            add_data_labels(_ax_, config['data_labels'], type=config[y]['graph_type'])

    # show legend
    add_legend(ax, fig, config['legend'])

    # set plot title
    add_title()

    # set output name from input, if output field is empty
    if len(output) <= 0:
        output = '.'.join(input.split('.')[:-1]) + '.png'
    #plt.show()
    plt.savefig(output, bbox_inches='tight', dpi=config['quality_in_dpi'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conf', dest='conf', default='config.yaml', help='yaml file defining configuration')
    args = parser.parse_args()
    config = load_yaml_file(args.conf)

    # get standard colors list
    color_palette = list(mcolors.TABLEAU_COLORS.keys())

    _axes_ = [ key for key in config.keys() if key.endswith('_y')]  #['primary_y', 'secondary_y']
    validate_config(config)
    render_graph(config, config['input'], config['output'])
