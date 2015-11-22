
class DTW_Sakoe_Chiba extends DTW {
	
	public float calculateDTW(float training_series[], float test_series[], float displacement){
		float[][] m = new float[training_series.length + 1][test_series.length + 1];
	
		for(int i = 0; i <= training_series.length; i++){
			for(int j = 0; j <= test_series.length; j++)
				m[i][j] = Float.MAX_VALUE;
		}

		m[0][0] = 0F;

		int band = Math.round(displacement*test_series.length);

		for(int i = 1; i <= training_series.length; i++){
			for(int j = lowerBound(i, band); j <= upperBound(i, band, test_series.length); j++)
				m[i][j] = ((training_series[i-1] - test_series[j-1]) * (training_series[i-1] - test_series[j-1])) 
							+ min(m[i-1][j-1], m[i-1][j], m[i][j-1]);
		}

		return m[training_series.length][test_series.length];
	}

	private int lowerBound(int i, int band){
		return i - band > 0 ? (i - band) : i;
	}

	private int upperBound(int i, int band, int max){
		return i + band <= max ? i + band : max;
	}

}