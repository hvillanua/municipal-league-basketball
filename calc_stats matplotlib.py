# -*- coding: cp1252 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

import os, time
from datetime import datetime as dt

# These are the "Tableau 20" colors as RGB.
# When targeting a broad audience, it would be better
# to use a colorblind friendly schemes such as Tableau's Color Blind 10.
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

color_blind_10 = [(0, 107, 164), (255, 128, 14), (171, 171, 171), (89, 89, 89),
                  (95, 158, 209), (200, 82, 0), (137, 137, 137), (162, 200, 236),
                  (255, 188, 121), (207, 207, 207)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

def calc_stats_game(excel_file, sheets=None):

    if not os.path.exists(excel_file):
        print "Can't find file: ", excel_file
        return
    df = pd.read_excel(excel_file, sheetname=sheets)

    if type(df) == dict:
        keys = df.keys()
        for k in keys:
            sheet_df = df[k]
            sheet_name = k
            calc_shoots_game(sheet_df, sheet_name)
            calc_rebounds(sheet_df, sheet_name)
            calc_fouls(sheet_df, sheet_name)
    else:
        sheet_name = sheets
        calc_shoots_game(df, str(sheet_name))
        calc_rebounds(df, str(sheet_name))
        calc_fouls(df, str(sheet_name))


def calc_shoots_game(df, file_name):
    '''
    Plot 2, 3 point shoots and free throws
    '''
    # You typically want your plot to be ~1.33x wider than tall.
    # Common sizes: (10, 7.5) and (12, 9)
    plt.figure(figsize=(12, 9))

    # Remove the plot frame lines. They are unnecessary chartjunk.
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Ensure that the axis ticks only show up on the bottom and left of the plot.
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    df_2_3_points = df[['Nombre', '2p m', '2p f', '2p %', '3p m', '3p f', '3p %', 'TL m', 'TL f', 'TL %']][df['Nombre'] != 'TOTAL']
    df_2_3_points[['2p f', '3p f', 'TL f']] = -df_2_3_points[['2p f', '3p f', 'TL f']]
    num_players = df_2_3_points['Nombre'].count()
    max_points = int(max(df_2_3_points[['2p m', '3p m', 'TL m']].max()))
    min_points = int(min(df_2_3_points[['2p f', '3p f', 'TL f']].min()))
    ind = np.arange(0, num_players, 1)
    width = 0.30
    bar_width = width*2/3

    # Limit the range of the plot to only where the data is.
    # Avoid unnecessary whitespace.
    plt.xlim(-width,len(ind)+width)
    #plt.ylim(63, 85)

    # Make sure your axis ticks are large enough to be easily read.
    # You don't want your viewers squinting to read your plot.
    plt.xticks(ind+width, fontsize=14)
    plt.yticks(range(min_points, max_points+1, 1), fontsize=12)

    ax.set_xticklabels(tuple(df_2_3_points['Nombre']), fontsize=12)

    # Provide tick lines across the plot to help your viewers trace along
    # the axis ticks. Make sure that the lines are light and small so they
    # don't obscure the primary data lines.
    # This is useful when using the standard matplotlib style.
    # Ggplot style seems to better suit without needing to print tick lines
    #for y in range(0, max_points+1, 1):
    #    plt.plot(range(0, num_players+1, 1), [y] * len(range(0, num_players+1, 1)), "--", lw=0.5, color="black", alpha=0.3)

    # Along the same vein, make sure your axis labels are large
    # enough to be easily read as well. Make them slightly larger
    # than your axis tick labels so they stand out.
    #plt.xlabel("Jugador", fontsize=16)
    #plt.ylabel("Canastas", fontsize=16)

    # Make the title big enough so it spans the entire plot, but don't make it
    # so big that it requires two lines to show.
    #plt.title("Aciertos y fallos", fontsize=22)

    # Choice of colors: darksage, steelblue, gold
    
    p1 = plt.bar(ind, df_2_3_points['2p m'], bar_width, color=tableau20[0], alpha=1.)
    p2 = plt.bar(ind, df_2_3_points['2p f'], bar_width, color=tableau20[0], alpha=0.5)
    p3 = plt.bar(ind+bar_width, df_2_3_points['3p m'], bar_width, color=tableau20[4], alpha=1.)
    p4 = plt.bar(ind+bar_width, df_2_3_points['3p f'], bar_width, color=tableau20[4], alpha=0.5)
    p5 = plt.bar(ind+2*bar_width, df_2_3_points['TL m'], bar_width, color=tableau20[6], alpha=1.)
    p6 = plt.bar(ind+2*bar_width, df_2_3_points['TL f'], bar_width, color=tableau20[6], alpha=0.5)

    # Always include your data source(s) and copyright notice! And for your
    # data sources, tell your viewers exactly where the data came from,
    # preferably with a direct link to the data. Just telling your viewers
    # that you used data from the "U.S. Census Bureau" is completely useless:
    # the U.S. Census Bureau provides all kinds of data, so how are your
    # viewers supposed to know which data set you used?
    #plt.text(0, min_points*1.2, u"\nAuthor: Hugo Villanúa Vega (https://github.com/hvillanua)", fontsize=10)
    plt.figtext(.1, -.005, u"\nAuthor: Hugo Villanúa Vega (https://github.com/hvillanua)", fontsize=10)
    
    # Add a legend only if necessary, we don't want to saturate the graphic
    ax.legend((p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]), ('2p metidos', '2p fallados', '3p metidos', '3p fallados', 'Tiros libres metidos', 'Tiros libres fallados'), loc='center left', bbox_to_anchor=(1, 0.5))
      
    # Finally, save the figure as a PNG.
    # You can also save it as a PDF, JPEG, etc.
    # Just change the file extension in this call.
    # bbox_inches="tight" removes all the extra whitespace on the edges of your plot.
    plt.savefig("Tiros_" + file_name + ".png", bbox_inches="tight")

    #plt.show()

    '''
    for i, name in zip(range(num_players), df_2_3_points['Nombre']):
        row = df_2_3_points[df_2_3_points['Nombre'] == name]
        perc_2p = float(row['2p %'])
        perc_3p = float(row['3p %'])
        perc_ft = float(row['TL %'])
        perc_2p_text = ''
        perc_3p_text = ''
        perc_ft_text = ''
        y_offset = -.13
        points_2p = float(row['2p m'])
        points_3p = float(row['3p m'])
        points_ft = float(row['TL m'])
        if np.isnan(perc_2p):
            perc_2p_text = ' N/A '
        else:
            perc_2p_text = "{0:.2%}".format(perc_2p)
        if np.isnan(perc_3p):
            perc_3p_text = ' N/A '
        else:
            perc_3p_text = "{0:.2%}".format(perc_3p)
        if np.isnan(perc_ft):
            perc_ft_text = ' N/A '
        else:
            perc_ft_text = "{0:.2%}".format(perc_ft)

        ax.text(i, points_2p if not np.isnan(points_2p) else 0, perc_2p_text, fontsize=9)
        ax.text(i+bar_width, (points_3p if not np.isnan(points_3p) else 0) + y_offset, perc_3p_text, fontsize=9)
        ax.text(i+2*bar_width, points_ft if not np.isnan(points_ft) else 0, perc_ft_text, fontsize=9)
        #ax.annotate(perc_2p, xy=(i, row['2p m']), xytext=(i, row['2p m']))
        #ax.annotate(perc_3p, xy=(i+width, row['3p m']), xytext=(i+width, row['3p m']))

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
    ax.legend((p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]), ('2p metidos', '2p fallados', '3p metidos', '3p fallados', 'Tiros libres metidos', 'Tiros libres fallados'), loc='center left', bbox_to_anchor=(1, 0.5))
    '''

def calc_rebounds(df, file_name):
    '''
    Plot rebounds
    '''
    # You typically want your plot to be ~1.33x wider than tall.
    # Common sizes: (10, 7.5) and (12, 9)
    plt.figure(figsize=(12, 9))

    # Remove the plot frame lines. They are unnecessary chartjunk.
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Ensure that the axis ticks only show up on the bottom and left of the plot.
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    df_rebounds = df[['Nombre', 'Reb Of', 'Reb Def']][df['Nombre'] != 'TOTAL']
    num_players = df_rebounds['Nombre'].count()
    max_rebounds = int(max(df_rebounds['Reb Of'].max(), df_rebounds['Reb Def'].max()))
    ind = np.arange(0, num_players, 1)
    width = 0.30
    bar_width = width*2/3

    # Limit the range of the plot to only where the data is.
    # Avoid unnecessary whitespace.
    plt.xlim(-width,len(ind)+width)
    #plt.ylim(63, 85)

    # Make sure your axis ticks are large enough to be easily read.
    # You don't want your viewers squinting to read your plot.
    plt.xticks(ind+width, fontsize=12)
    plt.yticks(range(0, max_rebounds+1, 1), fontsize=12)

    ax.set_xticklabels(tuple(df_rebounds['Nombre']), fontsize=12)

    # Along the same vein, make sure your axis labels are large
    # enough to be easily read as well. Make them slightly larger
    # than your axis tick labels so they stand out.
    #plt.xlabel("Jugador", fontsize=16)
    plt.ylabel("Rebotes", fontsize=16)

    # Make the title big enough so it spans the entire plot, but don't make it
    # so big that it requires two lines to show.
    #plt.title("", fontsize=22)

    # Choice of colors: darksage, steelblue, gold
    
    p1 = plt.bar(ind, df_rebounds['Reb Of'], width, color=tableau20[0], alpha=1.)
    p2 = plt.bar(ind+width, df_rebounds['Reb Def'], width, color=tableau20[4], alpha=1.)

    # Always include your data source(s) and copyright notice! And for your
    # data sources, tell your viewers exactly where the data came from,
    # preferably with a direct link to the data. Just telling your viewers
    # that you used data from the "U.S. Census Bureau" is completely useless:
    # the U.S. Census Bureau provides all kinds of data, so how are your
    # viewers supposed to know which data set you used?
    #plt.text(0, -.4, u"\nAuthor: Hugo Villanúa Vega (https://github.com/hvillanua)", fontsize=10)
    plt.figtext(.1, -.005, u"\nAuthor: Hugo Villanúa Vega (https://github.com/hvillanua)", fontsize=10)
    
    # Add a legend only if necessary, we don't want to saturate the graphic
    ax.legend((p1[0], p2[0]), ('Rebotes ofensivos', 'Rebotes defensivos'), loc='center left', bbox_to_anchor=(1, 0.5))
      
    # Finally, save the figure as a PNG.
    # You can also save it as a PDF, JPEG, etc.
    # Just change the file extension in this call.
    # bbox_inches="tight" removes all the extra whitespace on the edges of your plot.
    plt.savefig("Rebotes_" + file_name + ".png", bbox_inches="tight")

    #plt.show()

def calc_fouls(df, file_name):
    '''
    Plot fouls
    '''
    # You typically want your plot to be ~1.33x wider than tall.
    # Common sizes: (10, 7.5) and (12, 9)
    plt.figure(figsize=(12, 9))

    # Remove the plot frame lines. They are unnecessary chartjunk.
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Ensure that the axis ticks only show up on the bottom and left of the plot.
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    df_fouls = df[['Nombre', 'Faltas Rea']][df['Nombre'] != 'TOTAL']
    num_players = df_fouls['Nombre'].count()
    max_fouls = int(df_fouls['Faltas Rea'].max())
    ind = np.arange(0, num_players, 1)
    width = 0.30
    bar_width = width*2/3

    # Limit the range of the plot to only where the data is.
    # Avoid unnecessary whitespace.
    plt.xlim(-width,len(ind)+width)
    #plt.ylim(63, 85)

    # Make sure your axis ticks are large enough to be easily read.
    # You don't want your viewers squinting to read your plot.
    plt.xticks(ind+width, fontsize=12)
    plt.yticks(range(0, max_fouls+1, 1), fontsize=12)

    ax.set_xticklabels(tuple(df_fouls['Nombre']), fontsize=12)

    # Make the title big enough so it spans the entire plot, but don't make it
    # so big that it requires two lines to show.
    plt.title("Faltas realizadas", fontsize=22)

    # Choice of colors: darksage, steelblue, gold
    
    p1 = plt.bar(ind+width/2, df_fouls['Faltas Rea'], width, color=tableau20[0], alpha=1.)

    # Always include your data source(s) and copyright notice! And for your
    # data sources, tell your viewers exactly where the data came from,
    # preferably with a direct link to the data. Just telling your viewers
    # that you used data from the "U.S. Census Bureau" is completely useless:
    # the U.S. Census Bureau provides all kinds of data, so how are your
    # viewers supposed to know which data set you used?
    #plt.text(0, -.3, u"\nAuthor: Hugo Villanúa Vega (https://github.com/hvillanua)", fontsize=10)
    plt.figtext(.1, -.005, u"\nAuthor: Hugo Villanúa Vega (https://github.com/hvillanua)", fontsize=10)
      
    # Finally, save the figure as a PNG.
    # You can also save it as a PDF, JPEG, etc.
    # Just change the file extension in this call.
    # bbox_inches="tight" removes all the extra whitespace on the edges of your plot.
    plt.savefig("Faltas_" + file_name + ".png", bbox_inches="tight")

    #plt.show()

def calc_stats_season(clasif_csv_file, game_csv_file):

    if not os.path.exists(clasif_csv_file):
        print "Can't find file: ", clasif_csv_file
        return

    if not os.path.exists(game_csv_file):
        print "Can't find file: ", game_csv_file
        return

    # You typically want your plot to be ~1.33x wider than tall.
    # Common sizes: (10, 7.5) and (12, 9)
    plt.figure(figsize=(15, 9))

    # Remove the plot frame lines. They are unnecessary chartjunk.
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    #Remove the x axis since we're going to plot a table beneath the bar plot
    ax.get_xaxis().set_visible(False)

    # Ensure that the axis ticks only show up on the bottom and left of the plot.
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.
    #ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    #Read classification file and games files
    df_clasi = pd.read_csv(clasif_csv_file, sep=';')
    #Retrieve only valuable information regarding the group we're interested in
    df_clasi = df_clasi[['Codigo_equipo', 'Posicion', 'Puntos', 'Partidos_jugados', 'Partidos_ganados',
                        'Partidos_empatados', 'Partidos_perdidos', 'Goles_favor', 'Goles_contra', 'Nombre_equipo']][df_clasi['Codigo_grupo'] == 359]
    df_clasi['Partidos_ganados %'] = (df_clasi['Partidos_ganados']/df_clasi['Partidos_jugados']).astype(float)
    #Clean team names
    df_clasi['Nombre_equipo'] = df_clasi['Nombre_equipo'].apply(lambda x: x.strip())
    #Order by leaderboard position
    df_clasi.sort(['Posicion'], ascending=True, inplace=True)

    df_games = pd.read_csv(game_csv_file, sep=';')
    #Retrieve only valuable information regarding the group we're interested in
    df_games = df_games[['Jornada', 'Partido', 'Codigo_equipo1', 'Codigo_equipo2', 'Resultado1', 'Resultado2',
                        'Fecha', 'Estado', 'Equipo_local', 'Equipo_visitante']][df_games['Codigo_grupo'] == 359]
    #Clean team names. Since the lague is ongoing future matches have already
    #been filled with placeholder values we only need finished matches
    df_games['Equipo_local'] = df_games['Equipo_local'].apply(lambda x: x.strip())
    df_games['Equipo_visitante'] = df_games['Equipo_visitante'].apply(lambda x: x.strip())
    #local_date = dt.now().date()
    file_date = game_csv_file[-12:-4]
    file_date_dt = dt.strptime(file_date, "%Y%m%d")
    file_date = dt.strftime(file_date_dt, "%Y-%m-%d")
    df_games['Fecha'] = df_games['Fecha'].apply(lambda x: dt.strptime(x,"%Y-%m-%d"))
    df_games = df_games[df_games['Fecha'] < file_date_dt]
    
    num_teams = df_clasi['Codigo_equipo'].count()
    max_wins = max(df_clasi['Partidos_ganados'].max(), df_clasi['Partidos_perdidos'].max())
    ind = np.arange(num_teams)
    width = 1./3
    bar_width = width*2/3

    # Limit the range of the plot to only where the data is.
    # Avoid unnecessary whitespace.
    plt.xlim(0,len(ind))
    #plt.ylim(63, 85)

    # Make sure your axis ticks are large enough to be easily read.
    # You don't want your viewers squinting to read your plot.
    plt.xticks(ind, fontsize=10)
    plt.yticks(range(0, max_wins+1, 1), fontsize=14)

    #ax.set_xticklabels(tuple(df_clasi['Nombre_equipo']), rotation=20)

    # Make the title big enough so it spans the entire plot, but don't make it
    # so big that it requires two lines to show.
    #plt.title("", fontsize=22)

    # Choice of colors: darksage, steelblue, gold
    
    p1 = plt.bar(ind+width/2, df_clasi['Partidos_ganados'], width, color=tableau20[0], alpha=1.)
    p2 = plt.bar(ind+width*3/2, df_clasi['Partidos_perdidos'], width, color=tableau20[6], alpha=1.)

    #Fill cells with results from games
    cell_text = [["" for i in range(num_teams)] for i in range(num_teams)]
    for i in range(num_teams): cell_text[i][i] = '-'
    teams_list = list(df_clasi['Nombre_equipo'])
    for i, row in df_games.iterrows():
        local_team = row['Equipo_local']
        visiting_team = row['Equipo_visitante']
        if (local_team == 'DESCANSA' or visiting_team == 'DESCANSA'): continue
        local_index = teams_list.index(local_team)
        visiting_index = teams_list.index(visiting_team)
        if not cell_text[local_index][visiting_index]:
            cell_text[local_index][visiting_index] = str(row['Resultado2']) + '-' + str(row['Resultado1'])
            cell_text[visiting_index][local_index] = str(row['Resultado1']) + '-' + str(row['Resultado2'])
        else:
            cell_text[local_index][visiting_index] += '\n' + str(row['Resultado2']) + '-' + str(row['Resultado1'])
            cell_text[visiting_index][local_index] += '\n' + str(row['Resultado1']) + '-' + str(row['Resultado2'])

    #Prepare colors
    colors = []
    #Prepare team names
    teams_list = list(df_clasi['Nombre_equipo'])

    #Fix for a team name too long to fit in the plot. It will be necessary
    #to create a function to check for long names and divide them into smaller chunks
    #so they can fit in the plot nicely.
    teams_list[teams_list.index('RESTAURANTE EL COSACO')] = 'RESTAURANTE\nEL COSACO'

    
    # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text,
                          rowLabels=teams_list,
                          #rowColours=colors,
                          colLabels=teams_list,
                          cellLoc='center',
                          loc='bottom')

    table_props = the_table.properties()
    table_cells = table_props['child_artists']
    cell_height = .1
    for cell in table_cells: cell.set_height(cell_height)
    
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(8)
    # Adjust layout to make room for the table:
    plt.subplots_adjust(left=0.2, bottom=0.2)

    # Always include your data source(s) and copyright notice! And for your
    # data sources, tell your viewers exactly where the data came from,
    # preferably with a direct link to the data. Just telling your viewers
    # that you used data from the "U.S. Census Bureau" is completely useless:
    # the U.S. Census Bureau provides all kinds of data, so how are your
    # viewers supposed to know which data set you used?
    plt.text(-.3, -max_wins*1.1, "\nData source: http://datos.madrid.es/portal/site/egob\n"
             "Name: \"Deportes: Juegos Deportivos Municipales. Temporada 2015 / 2016. Deportes colectivos\" | "
             "Last update: " + file_date + "\n"
             u"Author: Hugo Villanúa Vega (https://github.com/hvillanua)", fontsize=10)

    ax.legend((p1[0], p2[0]), ('Partidos ganados', 'Partidos perdidos'), loc='center left', bbox_to_anchor=(-0.25, 0.5))
      
    # Finally, save the figure as a PNG.
    # You can also save it as a PDF, JPEG, etc.
    # Just change the file extension in this call.
    # bbox_inches="tight" removes all the extra whitespace on the edges of your plot.
    plt.savefig("Clasificatoria_" + file_date + ".png", bbox_inches="tight")
    
    #plt.show()
