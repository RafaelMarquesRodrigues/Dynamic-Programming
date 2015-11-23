
class DTW_1D implements DTW {
	
	public float calculateDTW(float training_series[], float test_series[]){
		float[][] m = new float[training_series.length + 1][test_series.length + 1];
	
		for(int i = 0; i <= training_series.length; i++)
			m[i][0] = Float.MAX_VALUE;
		for(int i = 0; i <= test_series.length; i++)
			m[0][i] = Float.MAX_VALUE;

		m[0][0] = 0F;

		for(int i = 1; i <= training_series.length; i++){
			for(int j = 1; j <= test_series.length; j++)
				m[i][j] = ((training_series[i-1] - test_series[j-1]) * (training_series[i-1] - test_series[j-1])) 
							+ min(m[i-1][j-1], m[i-1][j], m[i][j-1]);
		}

		return m[training_series.length][test_series.length];
	}
}