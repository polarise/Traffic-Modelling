library( ggplot2 )

d <- read.table( "cumul_time.txt", stringsAsFactors=F )

p <- ggplot( d, aes( x=V1, y=V2, colour="Forward" )) + geom_line()
p <- p + geom_line( data=d, mapping=aes( x=V1, y=V3, colour="Reverse" ))
p <- p + scale_colour_hue( "Direction" )
p <- p + ggtitle( "Traffic Time Series" ) + xlab( "Time" ) + ylab( "Cumulative Time" )
p <- p + theme_bw()
p <- p + theme( plot.title=element_text( face="bold" ))

p

