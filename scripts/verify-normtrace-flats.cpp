#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <unordered_set>
#include <vector>

// Exact diagnostic of ALL F4-linear three-spaces in F65536, modulo nonzero
// scalar multiplication and binary Frobenius. Counts all their nonzero affine
// cosets in each cubic norm class. No polynomial-coefficient search.
constexpr unsigned P=0x1002d;
unsigned raw_mul(unsigned a,unsigned b){unsigned r=0;while(b){if(b&1)r^=a;b>>=1;a<<=1;if(a&65536)a^=P;}return r;}
std::array<unsigned,131070>ex;
std::array<unsigned,65536>lg;
unsigned mul(unsigned a,unsigned b){return a&&b?ex[lg[a]+lg[b]]:0;}
unsigned power(unsigned a,unsigned n){return a?ex[(uint64_t(lg[a])*n)%65535]:0;}
uint32_t key(unsigned a,unsigned b){return a|(b<<16);}
int main(int argc, char** argv){
 if(argc != 2){std::cerr << "Usage: verify-normtrace-flats OUTPUT.csv\n"; return 2;}
 unsigned z=1;for(unsigned i=0;i<65535;i++){assert(i==0||z!=1);ex[i]=z;lg[z]=i;z=raw_mul(z,2);}assert(z==1);
 for(unsigned i=65535;i<131070;i++)ex[i]=ex[i-65535];
 std::array<unsigned,4>E{0,1,ex[21845],ex[43690]};
 std::array<unsigned char,65536>N{};for(unsigned x=1;x<65536;x++)N[x]=1+lg[x]%3;
 // alpha^0,...,alpha^7 form an F4 basis: this is checked by enumeration.
 std::array<unsigned,8>base{};for(unsigned i=0;i<8;i++)base[i]=ex[i];
 std::array<bool,65536>basis_seen{};for(unsigned c=0;c<65536;c++){unsigned x=0;for(unsigned j=0;j<8;j++)x^=mul(E[(c>>(2*j))&3],base[j]);assert(!basis_seen[x]);basis_seen[x]=true;}
 std::unordered_set<uint32_t>visited;visited.reserve(1600000);
 std::ofstream representatives(argv[1]);
 assert(representatives.good());
 representatives<<"orbit,basis_a,basis_b,coefficient_16,coefficient_4,coefficient_1,normalized_orbit_size,maximum,coset,norm\n";
 std::array<unsigned,65536>seen{};unsigned stamp=0,planes=0,orbits=0,best=0;
 std::map<unsigned,unsigned>hist;
 auto row_options=[&](unsigned pivot,int other){
  std::vector<unsigned>rows{base[pivot+1]};
  for(unsigned col=pivot+1;col<7;col++)if(int(col)!=other){auto old=rows;rows.clear();for(auto c:E)for(auto x:old)rows.push_back(x^mul(c,base[col+1]));}
  return rows;
 };
 for(unsigned i=0;i<7;i++)for(unsigned j=i+1;j<7;j++){
  auto ar=row_options(i,j),br=row_options(j,-1);
  for(auto a:ar){unsigned t=power(a,4)^a,B=power(t,3),A=1^B;
   for(auto b:br){
    ++planes;unsigned s=power(b,16)^mul(A,power(b,4))^mul(B,b),s3=power(s,3);
    unsigned c16=power(A,4)^s3,c4=power(B,4)^mul(s3,A);
    if(visited.count(key(c16,c4)))continue;
    ++orbits;++stamp;std::vector<unsigned>U;for(auto u:E)for(auto v:E)for(auto w:E)U.push_back(u^mul(v,a)^mul(w,b));
    std::sort(U.begin(),U.end());assert(std::unique(U.begin(),U.end())==U.end());
    std::unordered_set<uint32_t>this_orbit;
    for(auto u:U){assert((power(u,64)^mul(c16,power(u,16))^mul(c4,power(u,4))^mul(1^c16^c4,u))==0);}
    assert((1^c16^c4)!=0);
    for(auto u:U)if(u&&u<mul(u,E[2])&&u<mul(u,E[3])){
     unsigned k16=c16?ex[(lg[c16]+65535-uint64_t(lg[u])*48%65535)%65535]:0;
     unsigned k4=c4?ex[(lg[c4]+65535-uint64_t(lg[u])*60%65535)%65535]:0;
     for(unsigned h=0;h<16;h++){this_orbit.insert(key(k16,k4));k16=power(k16,2);k4=power(k4,2);}
    }
    for(auto k:this_orbit){assert(!visited.count(k));visited.insert(k);}
    unsigned local=0,local_v=0,local_norm=0;
    for(unsigned v=0;v<65536;v++)if(seen[v]!=stamp){
     std::array<unsigned,4>count{};for(auto u:U){unsigned x=v^u;seen[x]=stamp;count[N[x]]++;}
     if(!v)continue;
     for(unsigned c=1;c<4;c++){if(count[c]>local){local=count[c];local_v=v;local_norm=E[c];}if(count[c]>best){best=count[c];std::cout<<"best "<<best<<" basis 1 "<<a<<" "<<b<<" coset "<<v<<" norm "<<E[c]<<" coefficients "<<c16<<" "<<c4<<" "<<(1^c16^c4)<<"\n"<<std::flush;}}
    }
    hist[local]++;
    representatives<<orbits<<","<<a<<","<<b<<","<<c16<<","<<c4<<","<<(1^c16^c4)<<","<<this_orbit.size()<<","<<local<<","<<local_v<<","<<local_norm<<"\n";
   }
  }
  std::cout<<"pivots "<<i<<" "<<j<<" normalized "<<planes<<" orbits "<<orbits<<" visited "<<visited.size()<<"\n"<<std::flush;
 }
 assert(planes==1490853);assert(visited.size()==planes);
 assert(orbits==4461);assert(best==40);assert(representatives.good());
 std::cout<<"complete planes "<<planes<<" orbits "<<orbits<<" maximum "<<best<<" orbit histogram";for(auto [k,v]:hist)std::cout<<" "<<k<<":"<<v;std::cout<<"\n";
}
