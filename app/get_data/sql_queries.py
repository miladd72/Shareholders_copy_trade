

primary_stocks_shareholders_change = """
WITH SharePercSum AS (
    SELECT 
        s.relatedDate,
        s.symbolId,
        SUM(s.sharePerc) AS totalSharePerc
    FROM 
        [SFGCOREDATA].[dbo].[TcTtHsStShareHolders] s
    WHERE 
        s.tradeType = 1 
    GROUP BY 
        s.relatedDate, s.symbolId
)
SELECT 
    s.relatedDate, 
    s.shareHolderCode, 
    s.shareHolderName, 
    ISNULL(s.sharePerc, 0) AS sharePerc,
    ISNULL(s.sharePercYest, 0) AS sharePercYest,
    s.symbolId, 
    sp.totalSharePerc,
    (ISNULL(s.sharePerc, 0) - ISNULL(s.sharePercYest, 0)) AS sharePercDiff, 
    sym.name
FROM 
    [SFGCOREDATA].[dbo].[TcTtHsStShareHolders] s
JOIN 
    [SFGCOREDATA].[dbo].[Symbol] sym ON s.symbolId = sym.primaryId AND sym.instrumentType = 1
JOIN
    SharePercSum sp ON s.relatedDate = sp.relatedDate AND s.symbolId = sp.symbolId
WHERE 
    (ISNULL(s.sharePerc, 0) - ISNULL(s.sharePercYest, 0)) != 0
ORDER BY 
    sharePercDiff DESC;
"""


primary_stocks_shareholders_change_with_features = """
WITH SharePercSum AS (
    SELECT 
        s.relatedDate,
        s.symbolId,
        SUM(s.sharePerc) AS totalSharePerc,
        COUNT(CASE WHEN s.shareHolderName = N'شخص حقیقی' THEN 1 END) AS countIndividualShareholders,
        COUNT(CASE WHEN s.shareHolderName != N'شخص حقیقی' THEN 1 END) AS countCorporateShareholders,
        SUM(CASE WHEN s.shareHolderName = N'شخص حقیقی' THEN ISNULL(s.sharePerc, 0) ELSE 0 END) AS percShareIndividual,
        SUM(CASE WHEN s.shareHolderName != N'شخص حقیقی' THEN ISNULL(s.sharePerc, 0) ELSE 0 END) AS percShareCorporate
    FROM 
        [SFGCOREDATA].[dbo].[TcTtHsStShareHolders] s
    WHERE 
        s.tradeType = 1 
    GROUP BY 
        s.relatedDate, s.symbolId
)
SELECT 
    s.relatedDate, 
    s.shareHolderCode, 
    s.shareHolderName, 
    ISNULL(s.sharePerc, 0) AS sharePerc,
    ISNULL(s.sharePercYest, 0) AS sharePercYest,
    s.symbolId, 
    sp.totalSharePerc,
    sp.countIndividualShareholders,
    sp.countCorporateShareholders,
    sp.percShareIndividual,
    sp.percShareCorporate,
    (ISNULL(s.sharePerc, 0) - ISNULL(s.sharePercYest, 0)) AS sharePercDiff, 
    sym.name
FROM 
    [SFGCOREDATA].[dbo].[TcTtHsStShareHolders] s
JOIN 
    [SFGCOREDATA].[dbo].[Symbol] sym ON s.symbolId = sym.primaryId AND sym.instrumentType = 1
JOIN
    SharePercSum sp ON s.relatedDate = sp.relatedDate AND s.symbolId = sp.symbolId
WHERE 
    (ISNULL(s.sharePerc, 0) - ISNULL(s.sharePercYest, 0)) != 0
ORDER BY 
    sharePercDiff DESC;

"""