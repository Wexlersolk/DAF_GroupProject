| Test                                       |   Statistic |       p-value | Threshold / Null          | Conclusion                    |
|:-------------------------------------------|------------:|--------------:|:--------------------------|:------------------------------|
| Multicollinearity (Max VIF)                |     1.10602 | nan           | < 5 (No issue)            | No multicollinearity in diffs |
| Breusch-Pagan (Heteroskedasticity)         |    24.8987  |   0.000145753 | H0: Homoskedasticity      | Reject H0 (Heteroskedastic)   |
| White Test (Heteroskedasticity)            |    47.242   |   0.00054289  | H0: Homoskedasticity      | Reject H0 (Heteroskedastic)   |
| Durbin-Watson (Autocorrelation)            |     1.63994 | nan           | ~ 2.0 (No autocorr)       | Mild positive autocorrelation |
| Breusch-Godfrey LM (Autocorrelation lag 4) |    47.6639  |   1.109e-09   | H0: No serial correlation | Reject H0 (Autocorrelated)    |
| Jarque-Bera (Normality of residuals)       |   898.044   |   9.8246e-196 | H0: Normal residuals      | Fat-tailed / Leptokurtic      |