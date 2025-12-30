#ifndef __STATES__
#define __STATES__

enum class TankMode {MANUAL, AUTOMATIC, UNCONNECTED, NOT_AVAILABLE};

/* Water level: L
   Caps: L1 and L2, with L1<L2
   TimeCaps: T1 and T2, with T1<T2

if (L>L1 and L<L2) for more than T1 time -> Water channel is 50% open until L<L1
if (L>L2) -> Water channel is 100% open ultil L<L2
*/
enum class WaterLevel {HALF, FULL, OTHER}; //! Possibly change
#endif