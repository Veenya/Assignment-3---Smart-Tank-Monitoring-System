// THIS IS A TEST FILE, if you want delete it
package org.mqttserver.policy;

public class PolicyDryRun {

    private static void print(SystemControllerImpl sc, String label) {
        System.out.println(label
                + " | wl=" + sc.getWl()
                + " | status=" + sc.getStatus()
                + " | valve=" + sc.getValveValue());
    }

    public static void main(String[] args) throws Exception {
        SystemControllerImpl sc = new SystemControllerImpl();

        // 1) sotto L1 => chiuso
        sc.setWL(0f);
        print(sc, "Case A (wl<=L1)");

        // 2) tra L1 e L2, ma NON ancora T1 => ancora chiuso
        sc.setWL(10f);
        print(sc, "Case B (between, before T1)");

        // aspetta un po' meno di T1 (se T1=6000ms, prova 3000)
        Thread.sleep(3000);
        sc.setWL(10f);
        print(sc, "Case C (still before T1)");

        // aspetta abbastanza per superare T1 (es: altri 4000 -> totale 7000)
        Thread.sleep(4000);
        sc.setWL(10f);
        print(sc, "Case D (after T1 -> 50%)");

        // 3) sopra L2 => immediato 100%
        sc.setWL(30f);
        print(sc, "Case E (wl>L2 -> 100%)");

        // 4) torna sotto L1 => chiude e reset timer
        sc.setWL(0f);
        print(sc, "Case F (back <=L1 -> close)");

        // 5) test UNCONNECTED: non chiamare setWL per >T2 e poi tickConnection()
        System.out.println("\n--- waiting to trigger UNCONNECTED ---");
        Thread.sleep(13000); // metti > T2 (se T2=12000ms)
        sc.tickConnection();
        print(sc, "Case G (UNCONNECTED)");

        // 6) ritorna online: arriva un nuovo wl
        sc.setWL(0f);
        print(sc, "Case H (reconnected)");
    }
}
