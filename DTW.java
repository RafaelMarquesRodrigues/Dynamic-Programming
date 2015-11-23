
interface DTW {
	public float calculateDTW(float training_series[], float test_series[]);

	default float min(float a, float b, float c){
		return a > b ? (b > c ? c : b) : (a > c ? c : a);
	}
}