package Lab4;

import java.util.HashMap;
import java.util.HashSet;

public class UnitProductiveRemove {
    public HashMap<String, HashSet<String>> productions;
    public String[] Vn,Vt;
    public boolean hasChanged=true;

    public UnitProductiveRemove(String[] Vn, String[] Vt,HashMap<String, HashSet<String>> productions){
        this.productions=productions;
        this.Vn=Vn;
        this.Vt=Vt;
        removeUnit();
        System.out.println("Step 5.2 Unit Removal:");
        System.out.println(productions);
        NonProductiveRemove nonProductiveRemove=new NonProductiveRemove(Vn,Vt,productions);
    }
    public void removeUnit(){
        while (hasChanged){
            hasChanged=false;

            for(String key:productions.keySet()){
                HashSet<String> set=productions.get(key);
                HashSet<String> tempset= new HashSet<>();
                HashSet<String> toRemove = new HashSet<>();
                for (String element:set){
                    if (element.length()==1 && Character.isUpperCase(element.charAt(0))){
                        hasChanged=true;
                        for(String element2:productions.get(element)){
                            tempset.add(element2);
                        }
                        toRemove.add(element);
                    }

                }
                for(String element:toRemove){
                    set.remove(element);
                }

                for (String element:tempset){
                    set.add(element);
                    System.out.println(key+": was added element:"+element);
                }
            }
        }
    }
}
