package Lab4;

import java.util.*;

public class CNF {
    List<String> Vn=new ArrayList<>();
    String[] Vt;
    HashMap<String, HashSet<String>> productions;
    HashMap<String, HashSet<String>> toRemove=new HashMap<>();
    HashMap<String, HashSet<String>> toAdd=new HashMap<>();
    HashMap<String,String> shortermap=new HashMap<>();
    HashMap<String,String> mask=new HashMap<>();
    boolean hasChanged=true;
    int j=1;
    String t = "X";
    String v = "W";
    public CNF(String[] Vn, String[] Vt, HashMap<String, HashSet<String>> productions){
        this.productions=productions;
        this.Vn.addAll(Arrays.asList(Vn));
        this.Vt=Vt;
        replaceWithNonTerminal();
        System.out.println("Step 5.2 Elimination of more than 2 non-terminal and addition of new productions:");
        eliminateNonterminals();
        System.out.println(productions);
    }

    public void eliminateNonterminals(){

        while (hasChanged){
            hasChanged=false;
            toRemove=new HashMap<>();
            toAdd=new HashMap<>();

            for (String key:productions.keySet()){
                for(String element:productions.get(key)){
                    if(element.length()>2 ){
                        HashSet<String> set = new HashSet<>();
                        HashSet<String> removeset= toRemove.get(key);
                        if(removeset==null){
                            removeset=new HashSet<>();
                            toRemove.put(key,removeset);
                        }
                        if(!shortermap.containsKey(element.substring(0,2))){
                            removeset.add(element);
                            shortermap.put(element.substring(0,2), t);
                            set.add(element.replace(element.substring(0,2), t ));}
                        else {
                            removeset.add(element);
                            String str=element.replace(element.substring(0,2),shortermap.get(element.substring(0,2)));
                            set.add(str);
                        }
                        toAdd.put(key,set);
                        if(element.length()>3 ){
                            HashSet<String> set2 = new HashSet<>();
                            HashSet<String> removeset2= toRemove.get(key);
                            if(removeset2==null){
                                removeset2=new HashSet<>();
                                toRemove.put(key,removeset2);
                            }
                            if(!shortermap.containsKey(element.substring(2,4))){
                                removeset2.add(element);
                                shortermap.put(element.substring(2,4), v);
                                set2.add(element.replace(element.substring(2,4), v ));}
                            else {
                                removeset2.add(element);
                                String str=element.replace(element.substring(2,4),shortermap.get(element.substring(2,4)));
                                set2.add(str);
                            }
                            toAdd.put(key,set2);
                        }
                    }
                }}

            for (String key:toRemove.keySet()){
                HashSet<String> setToAdd= toAdd.get(key);
                HashSet<String> setRemove=toRemove.get(key);
                for(String element:setRemove){
                    productions.get(key).remove(element);
                }
                for(String element:setToAdd){
                    productions.get(key).add(element);
                }
                for (String key2:shortermap.keySet()){
                    HashSet<String> set = new HashSet<>();
                    set.add(key2);
                    productions.put(shortermap.get(key2),set);
                }

            }
        }
    }
    public void replaceWithNonTerminal(){

        for(String key:productions.keySet()){
            if(j<key.charAt(0)){
                j=key.charAt(0);
            }
        }

        for(String terminal:Vt){
            mask.put(Character.toString((char) ++j),terminal);
        }
        for(String key:productions.keySet()){
            for(String element:productions.get(key)){
                String str = element;
                for(String keymask:mask.keySet()){
                    if(str.contains(mask.get(keymask))){
                        if(str.length()>1)
                            str=str.replace(mask.get(keymask),keymask);

                    }
                }
                HashSet<String> set=toRemove.get(key);
                if(set==null){
                    set=new HashSet<>();
                    toRemove.put(key,set);
                }
                set.add(element);
                set=toAdd.get(key);
                if(set==null){
                    set=new HashSet<>();
                    toAdd.put(key,set);
                }
                set.add(str);
                System.out.println(key+" -> "+element+": was replaced with: "+str);
            }
        }
        for(String key:toRemove.keySet()){
            for(String element:toRemove.get(key)){
                productions.get(key).remove(element);
            }
        }

        for(String key:toAdd.keySet()){
            for(String element:toAdd.get(key)){
                productions.get(key).add(element);
            }
        }

        for(String key:mask.keySet()){
            HashSet<String> set = new HashSet<>();
            set.add(mask.get(key));
            productions.put(key,set);
        }
        System.out.println("Step 5.1 Chomsky Normal Form");
        System.out.println(productions);

    }
}
