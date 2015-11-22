
class Movement {
	float series[];
	int type;

	Movement(float[] s, int t){
		type = t;
		series = s;
	}

	public float[] getSeries(){
		return series;
	}

	public int getType(){
		return type;
	}
}