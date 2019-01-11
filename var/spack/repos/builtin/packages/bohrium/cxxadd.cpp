#include <bhxx/bhxx.hpp>

int main() {
    const size_t dim = 3;
    bhxx::BhArray<double> a({dim});
    bhxx::BhArray<double> b({dim});
    bhxx::BhArray<double> c({dim});

    bhxx::identity(a, 1);
    bhxx::identity(b, 2);
    bhxx::add(c, a, b);

    bhxx::Runtime::instance().sync(c.base);
    bhxx::Runtime::instance().flush();

    for (auto it = c.data(); it < c.data() + dim; ++it) {
        if (*it != 3) {
            std::cout << "Failure, values not as expected." << std::endl;
            return 1;
        }
    }
    std::cout << "Success!" << std::endl;
    return 0;
}
