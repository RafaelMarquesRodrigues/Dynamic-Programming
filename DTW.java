
class DTW {
	public float min(float a, float b, float c){
		return a > b ? (b > c ? c : b) : (a > c ? c : a);
	}
}