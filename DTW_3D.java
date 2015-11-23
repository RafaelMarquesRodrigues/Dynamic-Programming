
class DTW_3D implements DTW {
	
	public float calculateDTW(float training_series[], float test_series[]){
		float[][] m = new float[(training_series.length/3) + 1][(test_series.length/3) + 1];
	
		for(int i = 0; i <= training_series.length/3; i++)
			m[i][0] = Float.MAX_VALUE;
		for(int i = 0; i <= test_series.length/3; i++)
			m[0][i] = Float.MAX_VALUE;

		m[0][0] = 0F;

		float aux;

		for(int i = 1; i <= training_series.length/3; i++){
			for(int j = 1; j <= test_series.length/3; j++){
				aux = 0;

				for(int k = 0; k < 3; k++)
					aux += ((training_series[((i-1)*3)+k] - test_series[((j-1)*3)+k]) 
						* (training_series[((i-1)*3)+k] - test_series[((j-1)*3)+k]));

				m[i][j] = aux + min(m[i-1][j-1], m[i-1][j], m[i][j-1]);
			}
		}

		return m[training_series.length/3][test_series.length/3];
	}
}