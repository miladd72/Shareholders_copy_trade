

primary_stocks_shareholders_change = """
    SELECT 
        s.relatedDate, s.shareHolderCode, s.shareHolderName, s.sharePercYest, s.sharePerc, s.symbolId, (s.sharePerc - s.sharePercYest) AS sharePercDiff, 
        sym.name
    FROM 
        [SFGCOREDATA].[dbo].[TcTtHsStShareHolders] s
    JOIN 
        [SFGCOREDATA].[dbo].[Symbol] sym ON s.symbolId = sym.primaryId AND sym.instrumentType = 1
    WHERE 
        (s.sharePerc - s.sharePercYest) != 0 AND s.tradeType = 1 
    ORDER BY 
       sharePercDiff DESC;

"""