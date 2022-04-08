package Lab4;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;


public class Main {

    public static String[] Vn;
    public static String[] Vt;
    public static HashMap<String, HashSet<String>> productions=new HashMap<String, HashSet<String>>();
    static String  nextline;
    static Scanner scanner;
    public static void main (String[] args) {
        try {
            File file = new File("C:\\Users\\Daniel\\IdeaProjects\\LFPC\\src\\Lab4\\Var20.txt");
            scanner = new Scanner(file);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        nextline = scanner.nextLine();
        Vn=nextline.split(" ");

        nextline = scanner.nextLine();
        Vt=nextline.split(" ");
        while (scanner.hasNextLine()){

            nextline=scanner.nextLine();
            String[] str=nextline.split(" ");
            HashSet<String> set= productions.get(str[0]);
            if(set==null){
                set=new HashSet<String>();
                productions.put(str[0],set);
            }
            for (int i = 1;i<str.length;i++) {
                set.add(str[i]);
            }

        }
        System.out.println(productions);
        EpsilonRemove epsilon = new EpsilonRemove(Vn, Vt, productions);

    }

}