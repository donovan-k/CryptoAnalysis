# CryptoAnalysis
Python code to perform various analysis on cryptocurrency

## Classes
#### CoinInfo
<pre>
> Creates dictionary of dataframes of information of daily information of cryptocurrency  
> such as opening price, closing price, high price, and low price  
> 
> PARAMETERS: 
> coins (array of strings) - name of coin ex: 'DOGE-USD' for doge coin  
> from_date (string) - date to find data from, in format 'yyyy-mm-dd'  
> end_date (string) - date to find data up to, in format 'yyyy-mm-dd' Default = today's date  
>   
> ATTRIBUTES:
> self.from_date - same as parameter  
> self.end_date - same as parameter  
> :var self.all_coin_data - (1) when len(coins) > 1: dictionary of dataframes holding coin data  
>                         - (2) when len(coins) == 1: dataframe of coins[0]'s coin data  
> 
> FUNCTIONS:
> get_coin_data(coin) - gets the coin's data from the pandas data reader  
> fetch_coin_data(coin) - gets the coin's data from the mega data (if read more than one coin)  


#### Analysis
> Performs analysis on coin's data such as the average direction index and others  
>   
> PARAMETERS:
> :param coin_data (dataframe) - holds information such as daily high, low, closing, and opening price  
>   
> FUNCTIONS:
> calculate_daily_adx(period=14) - Calculate the daily average directional movement value of a coin using periods of 'period' days  
</pre>
