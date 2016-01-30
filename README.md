# municipal-league-basketball
Script to generate plots for the municipal league and team averages per game.

I have been playing in the municipal basketball league of Madrid for two years now, and I thought that it might be interesting to have a script that would help my team to see how other teams progressed trough the season as well as their results.
I also added a script to plot some basic game statistics that we manually wrote each game.

Both the season and game schema are provided with headers writen in spanish. Below is a explanation of the game headers in english, but unfortunately I can not do the same for the season data as it is not under my control and may change the names or the schema at any time.

The input format for the season information comes from "http://datos.madrid.es/portal/site/egob".
Specifically under the section "Deportes: Juegos Deportivos Municipales. Temporada 20XX / 20XX. Deportes colectivos", where XX is the year of the ongoing season.
Take into acount that the script format may change without notice rendering this script useless, as it would need to be patched to match the new input format. The script has been tested for the 2015 - 2016 season.

The input format for the game statistics follows a simple tabular schema:
Nº | Nombre | Puntos | Band m | Band f | Band % | 2p m | 2p f | 2p % | 3p m | 3p f | 3p % | TL m | TL f | TL % | Reb Of | Reb Def | Asistencias | Recuper | Perdidas | Tap Rea | Tap Rec | Faltas Rec | Faltas Rea

English translation:
Nº | Name | Points | Layup s | Layup f | Layup % | 2p s | 2p f | 2p % | 3p s | 3p f | 3p % | FT m | FT f | FT % | Off Reb | Def Reb | Assists | Recov | Loss | Blo Mad | Blo Rec | Fouls Mad | Fouls Rec

Nº - Number of the player.
Nombre - Name of the player.
Puntos - Points score in the game.
Band m - Successful layups.
Band f - Failed layups.
Band % - Layup success (%).
2p m - Successful 2 point field goals.
2p f - Failed 2 point field goals.
2p % - Layup success (%).
3p m - Successful 3 point field goals.
3p f - Failed 2 point field goals.
3p % - Layup success (%).
TL m - Successful 2 point field goals.
TL f - Failed 2 point field goals.
TL % - Layup success (%).
Reb Of - Offensive rebounds.
Reb Def - Defensive rebounds
Asistencias - Assists.
Recuper - Recoveries.
Perdidas - Losses.
Tap Rea - Blocks made.
Tap Rec - Blocks received.
Faltas Rec - Fouls made.
Faltas Rea - Fouls received.
