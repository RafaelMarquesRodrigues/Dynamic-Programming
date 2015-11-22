
import java.util.ArrayList;
import java.util.HashMap;
import java.io.*;
import java.io.BufferedReader;

class Calculate {
	ArrayList<Movement> test;
	ArrayList<Movement> training;
	HashMap<Integer,String> label;

	public static void main(String[] args) {
		Calculate calculate = new Calculate();

		if(args.length > 1)
			calculate.begin(args[0], Float.parseFloat(args[1]));
		else
			calculate.begin(args[0], 0F);
	}

	public void begin(String type, float band){
		int hits = 0;

		test = new ArrayList<Movement>();
		training = new ArrayList<Movement>();
		label = new HashMap<Integer, String>();

		if(type.equals("1d") || type.equals("sc")){
			readSeriesFile("test.in", test);
			readSeriesFile("training.in", training);
			readLabel("label.in");
			
			if(type.equals("1d"))
				hits = startCalculation_1D();
			else if(type.equals("sc"))
				hits = startCalculation_Sakoe_Chiba(band);
		}
		else if(type.equals("3d")){
			readSeriesFile("test3D.in", test);
			readSeriesFile("training3D.in", training);
			readLabel("label3D.in");
			hits = startCalculation_3D();
		}
		else{
			System.out.println("Invalid option");
			return;
		}
		
		System.out.println(hits);
		System.out.println((hits)*1.0/test.size());
	}

	public void readLabel(String filename){
		try {
			BufferedReader br = new BufferedReader(new FileReader(filename));
			String str;

			while((str = br.readLine()) != null){
				String parts[] = str.split(" ");
				label.put(new Integer(Integer.parseInt(parts[0])), parts[1]);
			}

			br.close();
		}
		catch(IOException e){
			System.out.println("problem reading file");
		}		
	}

	public void readSeriesFile(String filename, ArrayList<Movement> list){
		try {
			BufferedReader br = new BufferedReader(new FileReader(filename));
			String str;

			while((str = br.readLine()) != null){
				String parts[] = str.split(" ");

				float[] array = new float[parts.length - 1];

				for(int i = 1; i < parts.length; i++)
					array[i-1] = Float.parseFloat(parts[i]);

				list.add(new Movement(array, Integer.parseInt(parts[0])));
			}

			br.close();
		}
		catch(IOException e){
			System.out.println("problem reading file");
		}
	}

	public int startCalculation_1D(){
		int hits = 0;
		int selectedType = -1;
		DTW_1D dtw = new DTW_1D();

		for(Movement test_series : test){
			float result = Float.MAX_VALUE;

			for(Movement training_series : training){
				float aux = dtw.calculateDTW(training_series.getSeries(), test_series.getSeries());
				
				if(result > aux){
					result = aux;
					selectedType = training_series.getType();
				}
			}

			if(selectedType == test_series.getType())
				hits++;
		}

		return hits;
	}

	public int startCalculation_Sakoe_Chiba(float band){
		int hits = 0;
		int selectedType = -1;
		DTW_Sakoe_Chiba dtw = new DTW_Sakoe_Chiba();

		for(Movement test_series : test){
			float result = Float.MAX_VALUE;

			for(Movement training_series : training){
				float aux = dtw.calculateDTW(training_series.getSeries(), test_series.getSeries(), band);
				
				if(result > aux){
					result = aux;
					selectedType = training_series.getType();
				}

			}

			if(selectedType == test_series.getType())
				hits++;
		}

		return hits;
	}

	public int startCalculation_3D(){
		int hits = 0;
		int selectedType = -1;
		DTW_3D dtw = new DTW_3D();

		for(Movement test_series : test){
			float result = Float.MAX_VALUE;

			for(Movement training_series : training){
				float aux = dtw.calculateDTW(training_series.getSeries(), test_series.getSeries());
				
				if(result > aux){
					result = aux;
					selectedType = training_series.getType();
				}
			}

			if(selectedType == test_series.getType())
				hits++;
		}

		return hits;
	}
}